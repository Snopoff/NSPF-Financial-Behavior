const express = require('express')
const cors = require('cors')
const {PythonShell} = require('python-shell');
const app = express()
const port = 3001

app.use(cors())

app.get('/state', (req, res) => {
        const {clientId} = req.query

        PythonShell.run('./scripts/state.py', {
            args:[clientId]
        }).then(messages=>{
            res.send(JSON.parse(messages))
        });
    }
)

app.get('/clients', (req, res) => {
        const {clientId} = req.query

        PythonShell.run('./scripts/clients.py', {
            args:[clientId]
        }).then(messages=>{
            res.send(JSON.parse(messages))
        });
    }
)

app.get('/clients-prediction', (req, res) => {
        const {clientId} = req.query

        PythonShell.run('./scripts/clients_prediction.py', {
            args:[clientId]
        }).then(messages=>{
            res.send(JSON.parse(messages))
        });
    }
)

app.get('/incomes', (req, res) => {
        const {clientId} = req.query

        PythonShell.run('./scripts/incomes.py', {
            args:[clientId]
        }).then(messages=>{
            res.send(JSON.parse(messages))
        });
    }
)

app.get('/incomes-prediction', (req, res) => {
        const {clientId} = req.query

        PythonShell.run('./scripts/incomes_prediction.py', {
            args:[clientId]
        }).then(messages=>{
            res.send(JSON.parse(messages))
        });
    }
)

app.get('/moex', (req, res) => {
        const {clientId} = req.query

        PythonShell.run('./scripts/moex.py', {
            args:[clientId]
        }).then(messages=>{
            res.send(JSON.parse(messages))
        });
    }
)

app.get('/unemployment', (req, res) => {
        const {clientId} = req.query

        PythonShell.run('./scripts/unemployment_level.py', {
            args:[clientId]
        }).then(messages=>{
            res.send(JSON.parse(messages))
        });
    }
)

app.get('/obl-price', (req, res) => {
        const {clientId} = req.query

        PythonShell.run('./scripts/obl_price.py', {
            args:[clientId]
        }).then(messages=>{
            res.send(JSON.parse(messages))
        });
    }
)

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})