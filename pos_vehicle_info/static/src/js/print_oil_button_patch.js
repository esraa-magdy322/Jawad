/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(PaymentScreen.prototype, {
    // Add method to be called after validate
    async _finalizeValidation() {
        await super._finalizeValidation(...arguments);
        
        // After validation, offer to print oil label if vehicle info exists
        const currentOrder = this.pos.get_order();
        if (currentOrder && currentOrder.track && currentOrder.next_track) {
            // Vehicle info exists, we can print later from invoice
            console.log("Vehicle info saved - can print from invoice");
        }
    }
});
