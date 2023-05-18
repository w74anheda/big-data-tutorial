
db.persons.aggregate([
    {
        $project: {
            birthday : {
                $convert : {
                    input: "$dob.date",
                    to : 'date'
                }
            }
        }
    }
])
