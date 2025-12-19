/** @odoo-module **/

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";
import { useState } from "@odoo/owl";

export class VehiclePopup extends AbstractAwaitablePopup {
    static template = "pos_vehicle_info.VehiclePopup";
    static defaultProps = {
        confirmText: _t("حفظ"),
        cancelText: _t("إلغاء"),
        title: _t("معلومات السيارة"),
        body: "",
    };

    setup() {
        super.setup();
        this.state = useState({
            plate_number: this.props.plate_number || "",
            car_type: this.props.car_type || "",
            car_model: this.props.car_model || 0,
            track: this.props.track || 0,
            next_track: this.props.next_track || 0,
        });
    }

    getPayload() {
        return {
            plate_number: this.state.plate_number,
            car_type: this.state.car_type,
            car_model: parseInt(this.state.car_model) || 0,
            track: parseInt(this.state.track) || 0,
            next_track: parseInt(this.state.next_track) || 0,
        };
    }
}
