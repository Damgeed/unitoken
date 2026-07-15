/* ── Ticker: KAIEX pattern — JS builds items, CSS animates ── */
(function(){
  var defaults = {
    balance: {label:'Balance', val:'0 GT'},
    spent:   {label:'Spent',   val:'$0.00'},
    models:  {label:'Models',  val:'0'},
    requests:{label:'API Calls', val:'0'},
    keys:    {label:'Active Keys', val:'0'},
    days:    {label:'Days Active', val:'0'},
    consumed:{label:'Tokens Used', val:'0'},
    status:  {label:'New API',  val:'● Standby'},
  };
  var keys = ['balance','spent','models','requests','keys','days','consumed','status'];

  function buildItems(){
    var inner = document.getElementById('tickerInner');
    if (!inner) return;
    var html = '';
    // Double for seamless scroll loop
    for (var r = 0; r < 2; r++) {
      for (var i = 0; i < keys.length; i++) {
        var k = keys[i];
        var d = defaults[k];
        html += '<span class="ticker-item" data-ticker="' + k + '">' +
          '<span class="ticker-label">' + d.label + '</span>' +
          '<span class="ticker-dot"></span>' +
          '<span class="ticker-value">' + d.val + '</span>' +
          '</span>';
      }
    }
    inner.innerHTML = html;
  }

  buildItems();

  /* ── Data updater ── */
  var tickerVals = {};

  function updateTicker(){
    var inner = document.getElementById('tickerInner');
    if (!inner) return;
    var items = inner.querySelectorAll('.ticker-item');
    for (var i = 0; i < items.length; i++) {
      var el = items[i];
      var key = el.getAttribute('data-ticker');
      if (!key) continue;
      var val = tickerVals[key] || defaults[key].val || '—';
      var vEl = el.querySelector('.ticker-value');
      if (vEl) vEl.textContent = val;
    }
  }

  function refreshTickerData(){
    var token = localStorage.getItem('gt_token');
    if (!token) return;

    if (typeof userData !== 'undefined' && userData){
      tickerVals['balance'] = (userData.token_balance || 0) + ' GT';
      tickerVals['spent'] = '$' + (userData.total_spent || 0).toFixed(2);
      updateTicker();
    }

    try {
      fetch('https://glbtoken-backend-production.up.railway.app/api/dashboard?days=1', {
        headers: {'Authorization': 'Bearer ' + token}
      }).then(function(r){ return r.json(); }).then(function(d){
        if (d && !d.error){
          tickerVals['balance'] = (d.token_balance || 0) + ' GT';
          tickerVals['spent'] = '$' + (d.total_spent || 0).toFixed(2);
          tickerVals['models'] = d.models_used || 0;
          tickerVals['requests'] = d.total_requests || 0;
          tickerVals['keys'] = d.api_keys_active || 0;
          tickerVals['days'] = d.days_active || 0;
          tickerVals['consumed'] = (d.total_tokens_consumed || 0).toLocaleString();
          tickerVals['status'] = d.newapi_connected ? '● Live' : '○ Standby';
          updateTicker();
        }
      }).catch(function(){});
    } catch(e){}

    setTimeout(refreshTickerData, 30000);
  }

  if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', refreshTickerData);
  } else {
    refreshTickerData();
  }
})();
