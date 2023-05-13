db.find(
    { $text: { $search: "red car" } },
    { score: { $meta: "text-score" } }
).sort({ score: { $meta: "textScore" } })