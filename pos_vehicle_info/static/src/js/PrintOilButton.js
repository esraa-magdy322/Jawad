/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(PaymentScreen.prototype, {
    async onClickPrintOilLabel() {
        const currentOrder = this.currentOrder;
        
        if (!currentOrder) {
            await this.popup.add(ErrorPopup, {
                title: _t("تنبيه"),
                body: _t("لا يوجد طلب حالي"),
            });
            return;
        }

        // Check if vehicle info is filled
        if (!currentOrder.track || !currentOrder.next_track) {
            await this.popup.add(ErrorPopup, {
                title: _t("معلومات ناقصة"),
                body: _t("الرجاء إدخال معلومات السيارة (الممشى والممشى القادم) أولاً من زر Vehicle"),
            });
            return;
        }

        try {
            // Prepare label data
            const labelData = {
                plate_number: currentOrder.plate_number || '',
                car_type: currentOrder.car_type || '',
                car_model: currentOrder.car_model || 0,
                track: currentOrder.track || 0,
                next_track: currentOrder.next_track || 0,
            };

            console.log('Printing label with data:', labelData);

            // Print label
            const result = await this.env.services.orm.call(
                "pos.order",
                "action_print_oil_label_from_pos",
                [],
                { label_data: labelData }
            );

            if (result && result.type === "ir.actions.report") {
                await this.env.services.action.doAction(result);
            }

            // Send WhatsApp if order has backend ID
            const orderId = currentOrder.id || currentOrder.server_id || currentOrder.backendId;
            console.log('Current order ID:', orderId, 'Type:', typeof orderId);
            
            if (orderId && orderId > 0) {
                console.log('Sending WhatsApp for order:', orderId);
                try {
                    const whatsappResult = await this.env.services.orm.call(
                        "pos.order",
                        "save_vehicle_data_and_send_whatsapp",
                        [orderId],
                        { label_data: labelData }
                    );
                    console.log('WhatsApp result:', whatsappResult);
                } catch (whatsappError) {
                    console.error('WhatsApp error:', whatsappError);
                }
            } else {
                console.log('No backend order ID - order not yet saved');
            }

        } catch (error) {
            console.error("Error printing oil label:", error);
            await this.popup.add(ErrorPopup, {
                title: _t("خطأ في الطباعة"),
                body: _t("حدث خطأ: ") + (error.message || error),
            });
        }
    },
});
