db.users.aggregate([
    {
        $lookup: {
            from: "orders",
            localField: "orders",
            foreignField: "_id",
            as: "user_orders"
        }
    }
]).pretty()