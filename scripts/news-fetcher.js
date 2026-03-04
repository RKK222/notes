#!/usr/bin/env node
/**
 * 新闻抓取和推送脚本
 * 功能：获取 A 股数据、财经、科技、国内外大事件新闻，推送到飞书群
 */

const { execSync } = require('child_process');
const path = require('path');
const https = require('https');

// 新闻源配置（权威来源）
const NEWS_SOURCES = {
  finance: [
    '华尔街见闻 最新财经新闻',
    '财新网 财经要闻',
    '彭博社 中文 财经',
    'Reuters 财经新闻',
    '新浪财经 头条'
  ],
  tech: [
    '36 氪 最新科技新闻',
    '虎嗅网 科技要闻',
    'TechCrunch 最新科技',
    'The Verge 科技新闻',
    '机器之心 AI 新闻'
  ],
  world: [
    '新华网 国内外大事',
    '人民网 要闻',
    'BBC 中文 新闻',
    '联合早报 国际新闻',
    '央视新闻 重要新闻'
  ]
};

/**
 * 获取 A 股实时数据
 * 数据源：腾讯财经
 */
async function getAStockData() {
  const stocks = [
    { name: '上证指数', code: 'sh000001' },
    { name: '深证成指', code: 'sz399001' },
    { name: '创业板指', code: 'sz399006' },
    { name: '上证 50', code: 'sh000016' }
  ];

  const results = {};

  for (const stock of stocks) {
    try {
      const url = `https://qt.gtimg.cn/q=${stock.code}`;
      const data = await new Promise((resolve, reject) => {
        https.get(url, (res) => {
          let chunk = '';
          res.on('data', (d) => chunk += d);
          res.on('end', () => {
            try {
              const match = chunk.match(/=~([~\d.]+)~/);
              if (match) {
                const parts = match[1].split('~');
                resolve({
                  current: parseFloat(parts[3]),
                  open: parseFloat(parts[4]),
                  high: parseFloat(parts[5]),
                  change: parseFloat(parts[3]) - parseFloat(parts[4]),
                  changePercent: ((parseFloat(parts[3]) - parseFloat(parts[4])) / parseFloat(parts[4]) * 100).toFixed(2)
                });
              } else {
                resolve(null);
              }
            } catch (e) {
              reject(e);
            }
          });
        }).on('error', reject);
      });

      if (data) {
        results[stock.name] = data;
      }
    } catch (error) {
      console.error(`获取 ${stock.name} 失败:`, error.message);
    }
  }

  return results;
}

function searchNews(query) {
  try {
    const cmd = `openclaw web_search --query "${query}" --count 5 --freshness "pd"`;
    const result = execSync(cmd, { encoding: 'utf-8', maxBuffer: 10 * 1024 * 1024 });
    return JSON.parse(result);
  } catch (error) {
    console.error(`搜索失败 ${query}:`, error.message);
    return [];
  }
}

function formatNewsItem(item, index) {
  return `${index + 1}. **${item.title}**\\n   ${item.snippet || ''}\\n   🔗 ${item.url}`;
}

function generateNewsReport() {
  const report = {
    finance: [],
    tech: [],
    world: []
  };

  console.log('📰 正在获取财经新闻...');
  for (const query of NEWS_SOURCES.finance) {
    const results = searchNews(query);
    if (results && results.length > 0) {
      report.finance.push(...results.slice(0, 2));
    }
  }

  console.log('💻 正在获取科技新闻...');
  for (const query of NEWS_SOURCES.tech) {
    const results = searchNews(query);
    if (results && results.length > 0) {
      report.tech.push(...results.slice(0, 2));
    }
  }

  console.log('🌍 正在获取国内外大事件...');
  for (const query of NEWS_SOURCES.world) {
    const results = searchNews(query);
    if (results && results.length > 0) {
      report.world.push(...results.slice(0, 2));
    }
  }

  return report;
}

function buildMessage(report, aStockData) {
  const now = new Date();
  const timeStr = now.toLocaleString('zh-CN', { 
    timeZone: 'Asia/Shanghai',
    month: 'numeric',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });

  let message = `📰 **新闻速递** - ${timeStr}\\n`;
  message += `━━━━━━━━━━━━━━━━━━\\n\\n`;

  // A 股市场数据
  if (aStockData && Object.keys(aStockData).length > 0) {
    message += `💰 **A 股市场**\\n`;
    for (const [name, data] of Object.entries(aStockData)) {
      const icon = data.change >= 0 ? '📈' : '📉';
      const sign = data.change >= 0 ? '+' : '';
      message += `${icon} **${name}**: ${data.current.toFixed(2)}点 (${sign}${data.change.toFixed(2)}, ${sign}${data.changePercent}%)\\n`;
    }
    message += `\\n`;
  }

  if (report.finance.length > 0) {
    message += `💰 **财经要闻**\\n`;
    report.finance.slice(0, 4).forEach((item, i) => {
      message += formatNewsItem(item, i) + '\\n\\n';
    });
  }

  if (report.tech.length > 0) {
    message += `💻 **科技前沿**\\n`;
    report.tech.slice(0, 4).forEach((item, i) => {
      message += formatNewsItem(item, i) + '\\n\\n';
    });
  }

  if (report.world.length > 0) {
    message += `🌍 **国内外大事**\\n`;
    report.world.slice(0, 4).forEach((item, i) => {
      message += formatNewsItem(item, i) + '\\n\\n';
    });
  }

  message += `\\n━━━━━━━━━━━━━━━━━━\\n`;
  message += `📌 **推送说明**\\n`;
  message += `- 更新频率：每日 07:00-21:00，每 2 小时一次\\n`;
  message += `- 信息来源：权威媒体 + 实时行情\\n`;
  message += `- 夜间静默：23:00-次日 07:00\\n\\n`;
  message += `_祝各位老板今天心情愉快，股票涨停，代码无 bug！_ 🚀`;
  
  return message;
}

function sendToFeishuGroup(message) {
  try {
    const cmd = `openclaw message send --channel feishu --target "chat:oc_1df73fc9673b4412982efa8601317d97" --message "${message.replace(/"/g, '\\"')}"`;
    execSync(cmd, { encoding: 'utf-8', stdio: 'inherit' });
    console.log('✅ 消息已推送到飞书群');
  } catch (error) {
    console.error('❌ 推送失败:', error.message);
    console.log('尝试使用 sessions_send...');
    
    try {
      const cmd = `openclaw sessions_send --label "news-push" --message "${message.replace(/"/g, '\\"')}"`;
      execSync(cmd, { encoding: 'utf-8', stdio: 'inherit' });
    } catch (e) {
      console.error('备用方案也失败了:', e.message);
      throw e;
    }
  }
}

// 主函数
async function main() {
  console.log('🚀 开始新闻抓取和推送任务...');
  console.log('='.repeat(50));
  
  try {
    console.log('📊 正在获取 A 股数据...');
    const aStockData = await getAStockData();
    
    console.log('📰 正在获取新闻...');
    const report = generateNewsReport();
    
    const message = buildMessage(report, aStockData);
    
    console.log('\\n📤 准备推送消息...');
    console.log('消息长度:', message.length, '字符');
    
    sendToFeishuGroup(message);
    
    console.log('\\n✅ 任务完成！');
  } catch (error) {
    console.error('\\n❌ 任务失败:', error.message);
    process.exit(1);
  }
}

main();
