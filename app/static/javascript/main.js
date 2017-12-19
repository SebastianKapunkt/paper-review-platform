$(function () {
    var loc = window.location.href; // returns the full URL
    if (/paper/.test(loc)) {
        $('#paper_link').addClass('active');
    }
    if (/submission/.test(loc)) {
        $('#submission_link').addClass('active');
    }
    if (/signup/.test(loc)) {
        $('#signup').addClass('active');
    }
    if (/signin/.test(loc)) {
        $('#signin').addClass('active');
    }
    if (/authored/.test(loc)) {
        $('#submitted').addClass('active');
        $('#overview').addClass('active');
    }
    if (/to_review/.test(loc)) {
        $('#to_review').addClass('active');
        $('#overview').addClass('active');
    }
    if (/conference_chair/.test(loc)) {
        $('#chair').addClass('active');
    }
    if (/admin/.test(loc)) {
        $('#admin').addClass('active');
    }
});

function selectAllOptions(select) {
    for (var i = 0; i < select.options.length; i++) {
        select.options[i].selected = true;
    }
}

function put(from, to) {
    let keep = [];
    for (let i = 0; i < from.options.length; i++) {
        if (from.options[i].selected === true) {
            var opt = document.createElement('option');
            opt.value = from.options[i].value;
            opt.innerHTML = from.options[i].innerHTML;
            to.appendChild(opt);
        } else {
            keep.push(from.options[i]);
        }
    }
    from.innerText = null;
    keep.forEach(element => from.options.add(element));
    sortSelect(to);
    sortSelect(from);
}

function sortSelect(selElem) {
    var tmpAry = new Array();
    for (var i = 0; i < selElem.options.length; i++) {
        tmpAry[i] = new Array();
        tmpAry[i][0] = selElem.options[i].text;
        tmpAry[i][1] = selElem.options[i].value;
    }
    tmpAry.sort();
    while (selElem.options.length > 0) {
        selElem.options[0] = null;
    }
    for (var i = 0; i < tmpAry.length; i++) {
        var op = new Option(tmpAry[i][0], tmpAry[i][1]);
        selElem.options[i] = op;
    }
    return;
}