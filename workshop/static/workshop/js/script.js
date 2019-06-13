
var ajaxModalGetForm = function(path, title, m=modal, query) {

  $.ajax({
    method: "GET",
    url: document.location.origin + path,
    data: query,
    cache: false,
    dataType: 'html',
  })
  .done((data) => {
    $('#modal-body').html(data);
    $('#modalTitle').html(title);
    m.form = $('#modalForm');
    $(m.window).modal('show');
  })
  .fail(()=>{
    $(m.message).addClass('alert-warning').html('You are not logged in').fadeIn(500);
    $(m.window).modal('show');
    setTimeout(()=>{
      $(m.window).modal('hide');
      m.reset();
    }, 1500);
  });
}

var ajaxModalPostForm = function(path, m=modal) {

    $.ajax({
      method: "POST",
      url: document.location.origin + path,
      dataType: "JSON",
      data: m.form.serialize(),
      beforeSend: () => {$('#modal-body').slideUp(500)},
    })
    .done((result) => {
            $(m.message).addClass('alert-success').html('Request accepted').fadeIn(500);
            setTimeout(()=>{
              $(m.window).modal('hide');
              m.reset();
            }, 1500);
    })
    .fail(()=>{
      $(m.message).addClass('alert-warning').html('Request failed').fadeIn(500);
      setTimeout(()=>{
        $(m.window).modal('hide');
        m.reset();
      }, 1000);

    });
}

var selectMenu = function() {
  Array.from(document.getElementById('top_navbar').getElementsByClassName('nav-item')).forEach((e)=>{
      if (document.location.pathname.includes(e.getAttribute('data'))) {
        e.classList.add('active');
        c = e.getElementsByClassName('nav-link');
        c[0].classList.add('active');
      };
  });
}

$(document).ready(function() {

  var modal = {};
  modal.window = document.getElementById('modalWindow');
  modal.message = $('#modal-message');
  $(modal.message).hide();
  modal.message.reset = () => {modal.message.removeClass('alert-warning alert-success alert-danger').html('').fadeOut()};
  modal.body = $('#modal-body');
  modal.body.reset = () => {modal.body.html('').fadeIn()};
  modal.reset = () => {
      modal.body.reset();
      modal.message.reset();
  }

  selectMenu();

  $('.add-customer').on('click', (e)=>{
    ajaxModalGetForm('/ajax/addCustomer', 'Add new Customer', modal);
    e.preventDefault();
  });

  $('.add-employee').on('click', (e)=>{
    ajaxModalGetForm('/ajax/addEmployee', 'Add new Employee', modal);
    e.preventDefault();
  });

  $('.add-vehicle').on('click', (e)=>{
    ajaxModalGetForm('/ajax/addVehicle', 'Add new Vehicle', modal);
    e.preventDefault();
  });

  $('.add-task').on('click', (e)=>{
    ajaxModalGetForm('/ajax/addTask', 'Add new Task', modal);
    e.preventDefault();
  });

  $('.add-invoice').on('click', (e)=>{
    let query = {'customer': e.target.getAttribute('data')}
    ajaxModalGetForm('/ajax/addInvoice', 'Add new Invoice', modal, query);
    e.preventDefault();
  });

  $('#modalSubmit').on('click', () => {
     ajaxModalPostForm(modal.form.attr('action'), modal);
  });
});
