const Models = require("./models");


function NewMenu(name, menu_obj) {
    let now = Date.now();
    let Menu = new Models.Menu({
        name: name,
        created_at: now,
        updated_at: now,
        menu: menu_obj,
    });
    return Menu;
}

// Testing code for MenuSchema
menu_obj = {
    test1: "Five",
    test2: [1,2,3,"Four"],
};

let Menu = NewMenu("Menu", menu_obj);
Menu.Create(function(error) {
    console.log("Menu Saved.");
    if (error) {
        console.error(error);
    }
});


Menu.FindByName(Menu.name, function(error, menus) {
    if (error) {
        console.error(error);
    }
    menus.forEach(function (value) {
        console.log(value);
    });
});
