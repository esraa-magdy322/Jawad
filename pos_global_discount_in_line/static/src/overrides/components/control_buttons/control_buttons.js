/** @odoo-module **/

import { DiscountButton } from "@pos_discount/overrides/components/discount_button/discount_button";
import { patch } from "@web/core/utils/patch";

patch(DiscountButton.prototype, {
    async apply_discount(pc) {
        // Check if global discount in line is enabled
        if (this.pos.config.global_discount_in_line) {
            // Apply discount to all order lines instead of adding discount product
            const order = this.pos.get_order();
            const lines = order.get_orderlines();

            for (const line of lines) {
                if (line.isGlobalDiscountApplicable && line.isGlobalDiscountApplicable()) {
                    line.set_discount(pc);
                }
            }
        } else {
            // Use the original discount method (adds discount product)
            return super.apply_discount(...arguments);
        }
    },
});
