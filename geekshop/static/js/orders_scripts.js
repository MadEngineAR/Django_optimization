window.onload = function () {
    let quantity, price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let quantity_arr = [];
    let price_arr = [];

    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());
//    console.log(total_forms)
    let order_total_cost = parseInt($('.order_total_cost').text().replace(',', '.')) || 0;
    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;

    console.log(order_total_cost, order_total_quantity)
    for (let i = 0; i < total_forms; i++) {
        quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val())
        price = parseInt($('input[name=orderitems-' + i + '-price]').val())
//        console.log(price)
        quantity_arr[i] = quantity;
        if (price) {
            price_arr[i] = price
        }else{
            price_arr[i] = 0;
        }
//        console.log(price_arr)
    }
//     console.info('PRICE', price_arr)
//     console.info('QUANTITY', quantity_arr)
    // 1 Method
    $('.order_form').on('click', 'input[type=number]', function(){
        let target = event.target
        orderitem_num = parseInt(target.name.replace('orderitems-','').replace('-quantity'))
//        console.log(orderitem_num)
        if (price_arr[orderitem_num]){
            orderitem_quantity = parseInt(target.value)
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num]
            quantity_arr[orderitem_num] = orderitem_quantity
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity)
    }

    })

    // 2 Method

     $('.order_form').on('click', 'input[type=checkbox]', function(){
        let target = event.target
        console.log(target)
        orderitem_num = parseInt(target.name.replace('orderitems-','').replace('-DELETE'))
        console.log(orderitem_num)
        if (target.checked){
            delta_quantity = - quantity_arr[orderitem_num]
        }else{
            delta_quantity = quantity_arr[orderitem_num]
        }
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity)
       })

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price*delta_quantity;
        order_total_cost = Number((order_total_cost+delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(order_total_cost.toString() + ',00');
    }

    $('.formset_row').formset({
    addText:'Добавить продукт',
    deleteText:'удалить',
    prefix:'orderitems',
    removed:deleteOrderItem,
    })


    function deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type="number"]').name
        orderitem_num = parseInt(target_name.replace('orderitems-','').replace('-quantity',''))
        delta_quantity = - quantity_arr[orderitem_num]
//      console.log(orderitem_num)
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity)
    }

    $('.order_form select').change(function(){
        let target =event.target;
//        console.log(target)
        let orderitem_num = parseInt(target.name.replace('orderitems-','').replace('-product',''));
//        console.log(orderitem_num)
        let orderitem_product_pk = target.options[target.selectedIndex].value;
        console.log(orderitem_product_pk);
        if(orderitem_product_pk) {
            $.ajax({
                url:'ordersapp/product/' + orderitem_product_pk + '/price/',
                success: function(data) {
                    let price_html = '<input type="text" name="orderitems-' + orderitem_num + '-price" value="'+data.price.toString() + '" class="form-control" id="id_orderitems-' + orderitem_num + '-price">'
                    let current_tr = $('order_form table').find('tr:eq('+(orderitem_num+1)+')');
                    console.log(current_tr)
                    current_tr.find('td:eq(2)').html(price_html)

                }


            })

        }



    })

}