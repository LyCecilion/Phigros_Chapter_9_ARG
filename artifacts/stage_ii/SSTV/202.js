(function () {
    fetch("state.php", {
        cache: "no-store",
    })
        .then(function (a) {
            return a.json();
        })
        .then(function (a) {
            if (a && a.sound === false) {
                location.replace("index.html" + location.search);
            }
        })
        .catch(function () {});
})();
