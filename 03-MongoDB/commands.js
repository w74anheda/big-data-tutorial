db.users.aggregate([
    { $lookup: { from: "orders", localField: "_id", foreignField: "user_id", as: "user_orders" } },
    { $unwind: "$user_orders" },
    { $lookup: { from: "product", localField: "user_orders.product_id", foreignField: "_id", as: "user_orders.product" } },
    {
        $group: {
            _id: "$_id",
            name: { $first: "$name" },
            orders: { $push: { "_id": "$user_orders._id", "product_id": "$user_orders.product_id", "quantity": "$user_orders.quantity" } }
        }
    }
]).pretty()