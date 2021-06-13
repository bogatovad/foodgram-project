function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

class Api {
    constructor(apiUrl) {
        this.apiUrl =  apiUrl;
    }
  getPurchases () {
    return fetch(`/api/v1/purchases/`, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addPurchases (id) {
    return fetch(`/api/v1/purchases/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie("csrftoken")
      },
      credentials: 'same-origin',
      body: JSON.stringify({
        id: id
      })
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          console.log(e)
          return Promise.reject(e.statusText)
      })
  }
  removePurchases (id){
    return fetch(`/api/v1/purchases/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie("csrftoken")
      },
      credentials: 'same-origin',
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addSubscriptions(id) {
    return fetch(`/api/v1/subscriptions/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie("csrftoken")
      },
      credentials: 'same-origin',
      body: JSON.stringify({
        id: id
      })
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  removeSubscriptions (id) {
    return fetch(`/api/v1/subscriptions/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie("csrftoken")
      },
      credentials: 'same-origin',
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addFavorites (id)  {
    return fetch(`/api/v1/favorites/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie("csrftoken")
      },
      credentials: 'same-origin',
      body: JSON.stringify({
        id: id
      })
    })
        .then( e => {
            if(e.ok) {
                return e.json()
            }
            return Promise.reject(e.statusText)
        })
  }
  removeFavorites (id) {
    return fetch(`/api/v1/favorites/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie("csrftoken")
      },
      credentials: 'same-origin',
    })
        .then( e => {
            if(e.ok) {
                return e.json()
            }
            return Promise.reject(e.statusText)
        })
  }
    getIngredients  (text)  {
        return fetch(`/api/v1/ingredients?query=${text}`, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then( e => {
                if(e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }
}
