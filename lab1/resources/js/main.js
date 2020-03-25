"use strict";

/**
 * Начальная инициализация критериев каждой из "площадок".
 *
 * @type {Area}
 */
let area1 = new Area([
    new Criterion({
        name: criterion1,
        mark: 2
    }),
    new Criterion({
        name: criterion2,
        mark: 3.5,
        mode: false
    }),
    new Criterion({
        name: criterion3,
        mark: 2,
        mode: false
    })
], 1);
let area2 = new Area([
    new Criterion({
        name: criterion1,
        mark: 5
    }),
    new Criterion({
        name: criterion2,
        mark: 1.8,
        mode: false
    }),
    new Criterion({
        name: criterion3,
        mark: 3,
        mode: false
    })
], 2);
let area3 = new Area([
    new Criterion({
        name: criterion1,
        mark: 1
    }),
    new Criterion({
        name: criterion2,
        mark: 4,
        mode: false
    }),
    new Criterion({
        name: criterion3,
        mark: 1,
        mode: false
    })
], 3);
let area4 = new Area([
    new Criterion({
        name: criterion1,
        mark: 3
    }),
    new Criterion({
        name: criterion2,
        mark: 3,
        mode: false
    }),
    new Criterion({
        name: criterion3,
        mark: 2,
        mode: false
    })
], 4);
let area5 = new Area([
    new Criterion({
        name: criterion1,
        mark: 1
    }),
    new Criterion({
        name: criterion2,
        mark: 3.5,
        mode: false
    }),
    new Criterion({
        name: criterion3,
        mark: 1,
        mode: false
    })
], 5);
let area6 = new Area([
    new Criterion({
        name: criterion1,
        mark: 4
    }),
    new Criterion({
        name: criterion2,
        mark: 4,
        mode: false
    }),
    new Criterion({
        name: criterion3,
        mark: 1,
        mode: false
    })
], 6);

let areas = [area1, area2, area3, area4, area5, area6];

normalCriterios();

/**
 * Привидения оценок критериев к безразмерному виду [0, 1]
 */
function normalCriterios() {
    for (let i = 0; i < areas[0].criterions.length; i++) {
        let val = areas[0].criterions[i].mark;
        areas.forEach(area => {
            if (area.criterions[i].mode) {
                val = val < area.criterions[i].mark ? area.criterions[i].mark : val;
            } else {
                val = val > area.criterions[i].mark ? area.criterions[i].mark : val;
            }
        });
        areas.forEach(area => {
            if (area.criterions[i].mode) {
                area.criterions[i].mark = area.criterions[i].mark / val;
            }  else {
                area.criterions[i].mark = val / area.criterions[i].mark;
            }
        });
    }
}

generateTable();

/**
 * Веса (оценка экспертов)
 * @type {*[]}
 */
let weights = RangMethod.calculate(
    [
        [1, 2, 3],
        [1, 3, 2]
    ]
);

/*
 * Adding zeros in start to numbers
 */
function setZeroFirstFormat(value)
{
    if (value < 10) {
        value = '0' + value;
    }
    return value;
}

function getDateTime() {
    let currentDateTime = new Date();
    let day = setZeroFirstFormat(currentDateTime.getDate());
    let month = setZeroFirstFormat(currentDateTime.getMonth() + 1);
    let year = currentDateTime.getFullYear();
    let hours = setZeroFirstFormat(currentDateTime.getHours());
    let minutes = setZeroFirstFormat(currentDateTime.getMinutes());
    let seconds = setZeroFirstFormat(currentDateTime.getSeconds());

    return day + "." + month + "." + year + " " + hours + ":" + minutes + ":" + seconds;
}

setInterval(function () {
    document.getElementById('time').innerHTML = getDateTime();
}, 1000);

let init = () => {

    console.log(areas.length);

    let pareto = new Pareto(areas);
    let pAreas = pareto.selectLotsOfPareto();

    console.log(pAreas);
    console.log(weights);
    let area = ElectreMethod.calculate(pAreas, weights);
    let msg = document.getElementById("msg");
    msg.innerHTML = "Наилучшей площадкой для строительства, является площадка №" + area.number;
};

function generateTable() {
    areas.forEach((area, index) => {
        document.querySelectorAll('#deliveryTermsRow td')[index + 1]
            .innerHTML = defineDeliveryTerms(area.criterions[0].relMark);
        document.querySelectorAll('#expensesRow td')[index + 1]
            .innerHTML = area.criterions[1].relMark;
        document.querySelectorAll('#pollutionHazardRow td')[index + 1]
            .innerHTML = definePollution(area.criterions[2].relMark);
    });
}

function defineDeliveryTerms(mark) {
    switch (mark) {
        case 1: return 'Средние';
        case 2: return 'Хорошие';
        case 3: return 'Хорошие (хуже чем в Пл1)';
        case 4: return 'Очень хорошие';
        case 5: return 'Отличные';
        default: return 'Не определены условия'
    }
}

function definePollution(mark) {
    switch (mark) {
        case 1: return 'Опасность мала';
        case 2: return 'Загрязнение возможно';
        case 3: return 'Высокая опасность';
        default: return 'Не определены условия'
    }
}

function selectPlace(id) {
    document.getElementById('editForm').style.display = '';
    document.getElementById('numberPlace').innerHTML = id + 1;
}

function acceptChange() {
    let placeIndex = parseInt(document.getElementById('numberPlace').innerHTML);
    let deliveryTerms = parseInt(document.querySelector('#editForm select[name="deliveryTerms"]').value);
    let expenses = parseInt(document.querySelector('#editForm input[name="expenses"]').value);
    let pollutionHazard = parseInt(document.querySelector('#editForm select[name="pollutionHazard"]').value);

    areas[placeIndex - 1] = new Area([
        new Criterion({
            name: criterion1,
            mark: deliveryTerms
        }),
        new Criterion({
            name: criterion2,
            mark: expenses,
            mode: false
        }),
        new Criterion({
            name: criterion3,
            mark: pollutionHazard,
            mode: false
        })
    ], placeIndex + 1);
    normalCriterios();
    generateTable();
    document.getElementById('editForm').style.display = 'none';
}