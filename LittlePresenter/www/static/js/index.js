
/*---------------------------------------------------------------------------------------------------------------------------
 * Humboldt-Institut's Little Presenter
 *
 * Copyright 2020 by Humboldt-Institut e.V. (https://www.humboldt-institut.org)
 *
 * This file is part of Humboldt-Institut's Little Presenter.
 *
 * Humboldt-Institut's Little Presenter is free software: you can redistribute it and/or modify it under the terms of the
 * GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Humboldt-Institut's Little Presenter is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
 * even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
 * for more details.
 *
 * You should have received a copy of the GNU General Public License along with Humboldt-Institut's Little Presenter. If not,
 * see <http://www.gnu.org/licenses/>.
 *
---------------------------------------------------------------------------------------------------------------------------*/

function call_api(api_function, callback) {
    const Http = new XMLHttpRequest();
    const url = '/api/' + api_function;
    Http.open("GET", url);
    Http.send();
    Http.onreadystatechange = (e) => {
        if (Http.readyState == 4 && Http.status == 200) {
            console.log(Http.responseText)
            callback();
        }
    }
}

function restart_presentation() {
    call_api('restart-presentation', function() {
        message_div = document.getElementById('restart_message');
        message_div.classList.remove("removed");
        message_div.classList.remove("hidden");
        window.setTimeout(function() {
            message_div = document.getElementById('restart_message');
            message_div.classList.add("removed");
            message_div.classList.add("hidden");
        }, 3000);
    });
}

function reboot_system() {
    call_api('reboot-system', function() {
        message_div = document.getElementById('reboot_message');
        message_div.classList.remove('removed');
        message_div.classList.remove('hidden');

        timer_div = document.getElementById('reboot_timer');
        timer_div.innerHTML = 90;
        window.setInterval(function() {
            timer_div = document.getElementById('reboot_timer');
            time = parseInt(timer_div.innerHTML);
            if (time > 0) {
                time -= 1;
                timer_div.innerHTML = time.toString();
            }
            else {
                tmp = window.location;
                window.location = tmp;
            }
        }, 1000);
    });
}

function highlight_upload() {
    button = document.getElementById('upload_button');
    spinner = document.getElementById('upload_spinner');
    button.classList.add('highlight');
    spinner.classList.remove('hidden');
}
