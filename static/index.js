function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function addItemToCart(itemId, view_url='add_to_cart/')
{
    const csrftoken = getCookie('csrftoken');
    itemId = itemId.replace('addToCardButton_', '')
    var xhr = new XMLHttpRequest();
    xhr.open('POST', view_url);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    var status = xhr.send(
    JSON.stringify(
      {
        'item_id' : itemId
      }, null, 2
    )
    );
    xhr.onload = () => {
      if (xhr.status == 200) {
            new Toast({
          title: false,
          text: 'Товар добавлен в корзину',
          theme: 'success',
          autohide: true,
          interval: 10000
        });
      }
      else {
            new Toast({
          title: false,
          text: 'Ошибка',
          theme: 'danger',
          autohide: true,
          interval: 10000
      });
      }
    };

}