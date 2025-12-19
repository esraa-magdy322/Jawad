/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    
    async onPrintOilLabel() {
        const currentOrder = this.pos.get_order();
        
        if (!currentOrder) {
            await this.popup.add(ErrorPopup, {
                title: _t("تنبيه"),
                body: _t("لا يوجد طلب حالي"),
            });
            return;
        }

        if (!currentOrder.track || !currentOrder.next_track) {
            await this.popup.add(ErrorPopup, {
                title: _t("معلومات ناقصة"),
                body: _t("الرجاء إدخال معلومات السيارة (الممشى والممشى القادم) أولاً"),
            });
            return;
        }

        try {
            const invoiceId = currentOrder.account_move;
            
            if (!invoiceId) {
                await this.popup.add(ErrorPopup, {
                    title: _t("خطأ"),
                    body: _t("لم يتم إنشاء فاتورة لهذا الطلب بعد. الرجاء التحقق من الدفع أولاً."),
                });
                return;
            }

            const result = await this.env.services.orm.call(
                "account.move",
                "action_print_oil_label",
                [invoiceId]
            );

            if (result && result.type === "ir.actions.report") {
                await this.env.services.action.doAction(result);
            }

        } catch (error) {
            console.error("Error printing oil label:", error);
            await this.popup.add(ErrorPopup, {
                title: _t("خطأ في الطباعة"),
                body: _t("حدث خطأ أثناء طباعة ملصق الزيت: ") + error.message,
            });
        }
    }
    
});
