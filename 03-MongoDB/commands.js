db.places.insertOne(
    {
        name: "Imam Khomeyni Hospital",
        point: {
            type: "Point",
            coordinates: [48.68601619690574, 31.32995237098178] // long/lat
        }
    }
)

db.places.find({
    point: {
        $near: {
            $geometry: {
                type: "Point",
                coordinates: [48.68701670610951, 31.328589484869]
            },
            $maxDistance: 180, //meter
            $minDistance: 10
        }
    }
})

db.places.createIndex({ point: "2dsphere" })