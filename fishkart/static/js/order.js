// foodkart/static/js/order.js
function writeOrder() {
    var info = JSON.parse(document.getElementById('info').textContent);
    var rests = JSON.parse(document.getElementById('rests').textContent);
    var payment_method = document.getElementById('payment_method').value;
    var shipping_info = {
        full_name: document.getElementById('full_name').value,
        email: document.getElementById('email').value,
        country: document.getElementById('country').value,
        address: document.getElementById('address').value,
        city: document.getElementById('city').value,
        postal_code: document.getElementById('postal_code').value,
        phone_number: document.getElementById('phone_number').value
    };

    // Validate data
    if (!info || !info.cust_id || !info.cust_name || !info.rest) {
        document.getElementById('msg').textContent = 'Error: Customer information is missing or no restaurants selected.';
        console.error('Invalid info:', info);
        return;
    }
    if (!rests || Object.keys(rests).length === 0) {
        document.getElementById('msg').textContent = 'Error: No items in the order.';
        console.error('Empty rests:', rests);
        return;
    }

    var i = 0;
    var jsonx = {};
    for (var k in rests) {
        if (!rests[k].rest_name || !rests[k].items || !rests[k].pickuplat || !rests[k].pickuplong || !rests[k].rest_id) {
            document.getElementById('msg').textContent = 'Error: Invalid restaurant data for ID ' + k;
            console.error('Invalid restaurant data:', rests[k]);
            return;
        }

        var key = firebase.database().ref('Orders/').push().key;
        jsonx[key] = {
            'rest_id': parseInt(rests[k].rest_id),
            'cust_id': parseInt(info.cust_id),
            'items': rests[k].items
        };

        firebase.database().ref('Orders/' + key).set({
            rest_id: parseInt(rests[k].rest_id),
            rest_name: rests[k].rest_name,
            pickuplat: parseFloat(rests[k].pickuplat),
            pickuplong: parseFloat(rests[k].pickuplong),
            item_list: rests[k].items,
            cust_id: parseInt(info.cust_id),
            cust_name: info.cust_name,
            del_lat: 0,
            del_long: 0,
            del_id: -1,
            curr_status: 0
        }).then(() => {
            i++;
            if (i === Object.keys(rests).length) {
                successfulorder({ rests: jsonx, payment_method: payment_method, shipping_info: shipping_info });
            }
        }).catch(error => {
            document.getElementById('msg').textContent = 'Error saving order: ' + error.message;
            console.error('Firebase error:', error);
        });
    }
}