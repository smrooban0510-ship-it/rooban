let moistureData = []

let tempData = []

let labels = []

// =================================================
// 📊 CHART SETUP
// =================================================

const ctx = document.getElementById('myChart')

const myChart = new Chart(ctx, {

    type: 'line',

    data: {

        labels: labels,

        datasets: [

            {

                label: 'Soil Moisture',

                data: moistureData,

                borderWidth: 3
            },

            {

                label: 'Temperature',

                data: tempData,

                borderWidth: 3
            }
        ]
    },

    options: {

        responsive: true
    }
})

// =================================================
// 🔄 LOAD DATA
// =================================================

async function loadData(){

    let response = await fetch("/data")

    let data = await response.json()

    // 🌱 Soil Moisture
    document.getElementById("moisture").innerText =
    data.moisture

    // 🌡️ Temperature
    document.getElementById("temperature").innerText =
    data.temperature + "°C"

    // 📏 Plant Height
    document.getElementById("height").innerText =
    data.height + " cm"

    // 🍂 Disease
    document.getElementById("disease").innerText =
    data.disease

    // 🌦️ Real Weather
    document.getElementById("weather").innerText =
    data.weather + " " + data.outside_temp + "°C"

    // 📍 City
    document.getElementById("city").innerText =
    data.city

    // 🌾 Harvest
    document.getElementById("harvest").innerText =
    data.harvest

    // 🧪 Fertilizer
    document.getElementById("fertilizer").innerText =
    data.fertilizer

    // 📸 Camera Refresh
    let img = document.querySelector("img")

    img.src = "/static/leaf.jpg?" + new Date().getTime()

    // =================================================
    // 📊 GRAPH UPDATE
    // =================================================

    let time =
    new Date().toLocaleTimeString()

    labels.push(time)

    moistureData.push(data.moisture)

    tempData.push(data.temperature)

    // Keep only 10 points
    if(labels.length > 10){

        labels.shift()

        moistureData.shift()

        tempData.shift()
    }

    myChart.update()
}

// Update every 60 seconds
setInterval(loadData,60000)

// First load
loadData()