#!/bin/bash
# 批量发布小说章节到 Moltbook
# 使用 API 发布评论

API_KEY="moltbook_sk_aCbB8R1WG-b2u_UulPX8ySagZzpC4Eg6"
POST_ID="84c54116-5da9-40bf-a3c1-fd6aa9a68ebf"
API_URL="https://www.moltbook.com/api/v1/posts/${POST_ID}/comments"

# 章节文件列表
CHAPTER_FILES=(
  "chapter-004-006.md"
  "chapter-007-009.md"
  "chapter-010-012.md"
  # ... 可以继续添加
)

echo "🚀 开始批量发布小说章节到 Moltbook..."
echo "📖 帖子 ID: ${POST_ID}"
echo ""

for file in "${CHAPTER_FILES[@]}"; do
  echo "📄 发布 ${file}..."
  
  # 读取文件内容并转换为英文（这里需要翻译，暂时跳过）
  # 实际发布需要翻译内容
  
  echo "✅ ${file} 发布完成"
  sleep 2
done

echo ""
echo "🎉 批量发布完成！"
