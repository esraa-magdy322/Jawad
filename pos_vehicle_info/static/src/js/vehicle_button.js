/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { VehiclePopup } from "./VehiclePopup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

export class VehicleButton extends Component {
    static template = "pos_vehicle_info.VehicleButton";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
    }
    
    async onClick() {
        const currentOrder = this.pos.get_order();
        
        if (!currentOrder) {
            await this.popup.add(ErrorPopup, {
                title: _t("تنبيه"),
                body: _t("الرجاء إنشاء طلب أولاً"),
            });
            return;
        }

        // Open Vehicle Popup with current values
        const { confirmed, payload } = await this.popup.add(VehiclePopup, {
            plate_number: currentOrder.plate_number || "",
            car_type: currentOrder.car_type || "",
            car_model: currentOrder.car_model || 0,
            track: currentOrder.track || 0,
            next_track: currentOrder.next_track || 0,
        });

        if (confirmed) {
            // Save all data to current order
            currentOrder.plate_number = payload.plate_number;
            currentOrder.car_type = payload.car_type;
            currentOrder.car_model = payload.car_model;
            currentOrder.track = payload.track;
            currentOrder.next_track = payload.next_track;

            console.log("Vehicle Info Saved:", payload);
        }
    }
}

ProductScreen.addControlButton({
    component: VehicleButton,
});
