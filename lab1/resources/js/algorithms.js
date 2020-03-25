"use strict";

const criterion1 = "Условие для доставки сырья";
const criterion2 = "Затраты на подготовку к строительству";
const criterion3 = "Опасность загрязнения грунтовых вод в слуае аварии";

/**
 * Класс описывающий площадку. Состоит из множества критериев.
 *
 * @author Evgeniy Trofimov
 * @version 1.0
 */
class Area {

    /**
     *
     * @param option
     * @param number
     */
    constructor(option, number) {
        this.criterions = option;
        this._number = number;
    }

    get criterions() {
        return this._criterions;
    }

    /**
     *
     * @param value {Array}
     */
    set criterions(value) {
        this._criterions = value;
    }
    get number() {
        return this._number;
    }

    /**
     *
     * @param criterion {Criterion}
     */
    add(criterion) {
        this.criterions.push(criterion);
    }

    /**
     * true - если больше по всем критериям.
     * false - иначе.
     * @param area
     * @return {boolean}
     */
    toCompare(area) {
        let check = true;
        if (this.criterions.length !== area.criterions.length) return false;
        for (let i = 0; i < this.criterions.length; i++) {
            check &= this.criterions[i].mark >= area.criterions[i].mark;
        }
        return check;
    }

    toString() {
        return "Area [\n" + this.criterions.forEach(c => c.toString() + ", ") + "]";
    }
}

/**
 * <h1>Класс описывающий критерий выбора</h1>
 *
 * @field mame {String} название критерия
 * @field mark {Integer} приоритет
 * @field mode {Boolean} метод оценки (true - по возрастанию, false - по убыванию)
 *
 * @author Evgeniy Trofimov
 * @version 1.0
 */
class Criterion {
    /**
     *
     * @param option {Object}
     */
    constructor(option) {
        if (option.name) this._name = option.name;
        if (option.mark) {
            this._mark = option.mark;
            this.relMark = option.mark;
        }
        if (option.mode !== undefined) this._mode = option.mode;
        else this._mode = true;
    }

    get name() {
        return this._name;
    }
    set name(value) {
        this._name = value;
    }
    get mark() {
        return this._mark;
    }
    set mark(value) {
        this._mark = value;
    }
    get mode() {
        return this._mode;
    }
    set mode(value) {
        this._mode = value;
    }

    toString() {
        return "Criterion [name = " + this.name + ",\n" +
            "mark = " + this.mark + ",\n" +
            "mode = " + this.mode + "]";
    }
}


class Pareto {
    /**
     *
     * @param areas {Array<Area>}
     */
    constructor(areas) {
        this._areas = areas;
    }

    add(area) {
        this._areas.push(area);
    }

    /**
     *
     * @return {[]}
     */
    selectLotsOfPareto() {
        let newAres = new Set(this._areas);
        for (let i = 0; i < this._areas.length; i++) {
            for (let j = i + 1; j < this._areas.length; j++) {
                if (this._areas[i].toCompare(this._areas[j])) {
                    newAres.delete(this._areas[j]);
                } else if (this._areas[j].toCompare(this._areas[i])) {
                    newAres.delete(this._areas[i]);
                }
            }
        }
        let array = [];
        newAres.forEach(a => array.push(a));
        return array;
    }
}


/**
 * Класс вычисляющий веса критериев по методу "Ранга". Критерий имеющий
 * максимальный вес, является более предпочтителен.
 *
 * @author Evgeniy Trofimov
 * @version 1.0
 */
class RangMethod {
    /**
     *
     * @param marks {[Int32Array]} оценки экспертов (строки - эксперты, столбцы - критерии)
     * @return {[]} весса критериев (алтернотив)
     */
    static calculate(marks) {
        let c = [];
        let m = marks.length;
        let n = marks[0].length;
        let marksSum = 0;  // C - сумма всех оценок
        for (let j = 0; j < n; j++) {
            let sum = 0;
            for (let i = 0; i < m; i++) {
                sum = marks[i][j];
            }
            c.push(sum);
            marksSum += sum;
        }
        let weights = [];
        c.forEach(el => weights.push(el / marksSum));
        return weights;
    }
}

/**
 * @author Evgeniy Trofimov
 * @version 1.0
 */
class ElectreMethod {
    /**
     *
     * @param areas {Array<Area>}
     * @param weights {[]}
     */
    static calculate(areas, weights) {
        if (areas.length === 1) return areas[0];
        let n = areas.length;
        let m = weights.length;
        let betterAreas = [];
        for (let i = 0; i < n - 1; i++) {
            let c = 0;
            let p = 0;
            for (let j = 0; j < m; j++) {
                if (areas[i].criterions[j].mark > areas[i + 1].criterions[j].mark) {
                    c += areas[i].criterions[j].mark * weights[j];
                } else {
                    p += areas[i + 1].criterions[j].mark * weights[j];
                }
            }
            if (c > p) betterAreas.push(areas[i]);
            else betterAreas.push(areas[i + 1]);
        }
        if (betterAreas.length === 1) return betterAreas[0];
        else return ElectreMethod.calculate(betterAreas, weights);
    }
}
