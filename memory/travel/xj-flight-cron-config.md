# 十一新疆机票监控 - Cron 配置

## Cron 任务名称
`xj-flight-monitor`

## 当前状态
⏸️ 暂停（提前时间过长，航司尚未开放十一预订）

## 计划启动时间
2026-06-01（提前 4 个月开始监控）

## Cron 配置示例

```bash
# 6-7 月：每周一次（周一 9:00）
0 9 * * 1-7/14 cd /Users/kaka/.openclaw/workspace && /path/to/flight-monitor.sh

# 8 月：每周三次（周一/三/五 9:00）
0 9 * * 1,3,5/2 cd /Users/kaka/.openclaw/workspace && /path/to/flight-monitor.sh

# 9 月：每日监控（9:00 和 20:00）
0 9,20 * * 9 cd /Users/kaka/.openclaw/workspace && /path/to/flight-monitor.sh
```

## 推送渠道
- 飞书群聊：待配置
- 推送格式：详见任务配置

## 监控脚本位置
待创建：`/Users/kaka/.openclaw/workspace/scripts/flight-monitor.sh`

## 下次执行
2026-06-02 09:00（首次正式查询）
