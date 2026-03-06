# 定时任务监控清单

**最后更新**: 2026-03-06 09:35  
**配置备份**: `cron-jobs-backup.json`（已提交 git）

---

## 📋 任务列表

| 任务名 | 频率 | 状态 | 最后检查 |
|--------|------|------|---------|
| novel-write-ai-butler | 每小时 | ✅ 正常 | 09:00 |
| github-daily-explorer | 11:00, 19:00 | ✅ 正常 | 未运行 |
| news-push | 7,9,11,13,15,17,19,21 点 | ✅ 正常 | 09:00 |
| calendar-check | 08:00 | ⚠️ khal 未安装 | 08:00 失败 |
| memory-maintenance | 周日 02:00 | ✅ 正常 | 未运行 |

---

## ⚠️ 已知问题

1. **calendar-check**: khal 未安装，需要安装 caldav-calendar skill
2. **news-push**: 已修复 channel ID 配置，11:00 验证

---

## 🔍 每日检查清单

- [ ] 检查 cron 任务是否正常运行
- [ ] 检查 consecutiveErrors 是否为 0
- [ ] 检查推送是否正常到达
- [ ] 检查配置文件是否被修改

---

## 🛠️ 故障恢复

如果配置丢失：
```bash
# 从 git 恢复
cd /Users/kaka/.openclaw/workspace
git pull origin master
cp cron-jobs-backup.json /Users/kaka/.openclaw/cron/jobs.json
```

---

## 📊 配置持久性说明

- **enabled 状态**: 永久保持，不会自动禁用
- **consecutiveErrors**: 成功执行后自动清零
- **配置文件**: 已备份到 git，可恢复
- **推送目标**: oc_1df73fc9673b4412982efa8601317d97（当前群）
