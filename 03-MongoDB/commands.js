db.movies.updateMany(
    {},
    {
        $sum: { aaa: { $sum: ["$runtime", "$wieght"] } }
    }
)