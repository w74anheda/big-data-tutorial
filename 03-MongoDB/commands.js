debugger.createCollection(
    "colectionName",
    {
        capped: true,
        size: 10000,// document size byte
        max: 3 // document count
    }
)