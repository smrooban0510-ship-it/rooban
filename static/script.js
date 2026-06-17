async function loadData() {

    try {

        // ===============================
        // FETCH DATA FROM FLASK
        // ===============================

        let response = await fetch('/data');

        let data = await response.json();

        // ===============================
        // 🌱 SOIL MOISTURE
        // ===============================

        document.getElementById(
            "moisture"
        ).innerText =
        data.moisture;

        // ===============================
        // 🌡️ TEMPERATURE
        // ===============================

        document.getElementById(
            "temperature"
        ).innerText =
        data.temperature + " °C";

        // ===============================
        // 💧 HUMIDITY
        // ===============================

        document.getElementById(
            "humidity"
        ).innerText =
        data.humidity + " %";

        // ===============================
        // 📏 PLANT HEIGHT
        // ===============================

        document.getElementById(
            "height"
        ).innerText =
        data.height + " cm";

        // ===============================
        // 🍂 DISEASE DETECTION
        // ===============================

        document.getElementById(
            "disease"
        ).innerText =
        data.disease;

        // ===============================
        // 🌦️ WEATHER
        // ===============================

        document.getElementById(
            "weather"
        ).innerText =
        data.weather + " / " +
        data.outside_temp + " °C";

        // ===============================
        // ☔ RAIN ALERT
        // ===============================

        if(data.rain_alert == "Yes"){

            document.getElementById(
                "rain_alert"
            ).innerText =
                "⚠️ Rain Expected";

        }
        else{

            document.getElementById(
                "rain_alert"
            ).innerText =
                "✅ No Rain";

        }

        // ===============================
        // 📍 CITY
        // ===============================

        document.getElementById(
            "city"
        ).innerText =
        data.city;

        // ===============================
        // 🌾 HARVEST STATUS
        // ===============================

        document.getElementById(
            "harvest"
        ).innerText =
        data.harvest;

        // ===============================
        // 🧪 FERTILIZER
        // ===============================

        document.getElementById(
            "fertilizer"
        ).innerText =
        data.fertilizer;

        // ===============================
        // 📸 REFRESH CAMERA IMAGE
        // ===============================

        document.getElementById(
             "leafImage"
        ).src =
        "http://10.150.81.177:5001/camera" +
        new Date().getTime();
        // ===============================
        // 📊 UPDATE CHART
        // ===============================

        updateChart(

            data.moisture,

            data.temperature,

            data.height
        );

    }

    catch(error){

        console.log(
            "Dashboard Error:",
            error
        );

    }
}

// =======================================
// 📊 CHART JS
// =======================================

const ctx = document.getElementById(
    'myChart'
).getContext('2d');

const myChart = new Chart(ctx, {

    type: 'line',

    data: {

        labels: [],

        datasets: [

            {
                label: 'Soil Moisture',

                data: [],

                borderWidth: 3,

                tension: 0.4
            },

            {
                label: 'Temperature',

                data: [],

                borderWidth: 3,

                tension: 0.4
            },

            {
                label: 'Plant Height',

                data: [],

                borderWidth: 3,

                tension: 0.4
            }
        ]
    },

    options: {

        responsive: true,

        maintainAspectRatio: false,

        scales: {

            y: {

                beginAtZero: true
            }
        }
    }
});

// =======================================
// 📈 UPDATE CHART
// =======================================

function updateChart(

    moisture,

    temperature,

    height
){

    let time = new Date()
    .toLocaleTimeString();

    // ===============================
    // ADD NEW VALUES
    // ===============================

    myChart.data.labels.push(time);

    myChart.data.datasets[0]
    .data.push(moisture);

    myChart.data.datasets[1]
    .data.push(temperature);

    myChart.data.datasets[2]
    .data.push(height);

    // ===============================
    // KEEP ONLY LAST 10 VALUES
    // ===============================

    if(
        myChart.data.labels.length > 10
    ){

        myChart.data.labels.shift();

        myChart.data.datasets[0]
        .data.shift();

        myChart.data.datasets[1]
        .data.shift();

        myChart.data.datasets[2]
        .data.shift();
    }

    // ===============================
    // REFRESH GRAPH
    // ===============================

    myChart.update();
}

// =======================================
// 🚀 FIRST LOAD
// =======================================

loadData();

// =======================================
// 🔄 AUTO REFRESH
// =======================================

setInterval(loadData, 5000);