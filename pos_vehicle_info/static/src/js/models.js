/** @odoo-module **/

import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.plate_number = this.plate_number || '';
        this.car_type = this.car_type || '';
        this.car_model = this.car_model || 0;
        this.track = this.track || 0;
        this.next_track = this.next_track || 0;
    },

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.plate_number = this.plate_number;
        json.car_type = this.car_type;
        json.car_model = this.car_model;
        json.track = this.track;
        json.next_track = this.next_track;
        return json;
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.plate_number = json.plate_number || '';
        this.car_type = json.car_type || '';
        this.car_model = json.car_model || 0;
        this.track = json.track || 0;
        this.next_track = json.next_track || 0;
    },
});
