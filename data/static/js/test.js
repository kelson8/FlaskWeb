// Getting IP
// Moved out of HTML, this uses my Flask route '/proxy-ip' and depending on which one is set in the test_pages.py, this gets either
// the public IP behind Cloudflare or the public IP directly.
//async function getIP() {
//    try {
//        const response = await fetch('/proxy-ip');
//        const data = await response.json();
//
//        const ipElement = document.getElementById("ip");
//
//        // if (ipElement.hasAttribute('hidden')) {
//        //     ipElement.removeAttribute('hidden');
//        // } else {
//        //     ipElement.setAttribute('hidden', "");
//        // }
//
//        document.getElementById('ip').innerText = `Your public IP Address is: ${data.ip}`;
//    } catch (error) {
//        console.error('Error fetching IP address:', error);
//    }
//}

// This checks if the IPv6 address is valid.
function isValidIPv6(ip) {
    const ipv6Pattern = /^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|::|[0-9a-fA-F]{1,4}:[0-9a-fA-F]{1,4}:[0-9a-fA-F]{0,1}[0-9a-fA-F]{0,1}:[0-9a-fA-F]{1,4}$/;
    return ipv6Pattern.test(ip);
}

async function getIP() {
    try {
        const response = await fetch('/proxy-ip');
        const data = await response.json();

        // const ipElement = document.getElementById("ip");
        const ip4Element = document.getElementById("ipv4");
        const ip6Element = document.getElementById("ipv6");
        ip4Element.innerHTML = ""; // Clear previous content
        ip6Element.innerHTML = ""; // Clear previous content

        // Check whether IPv4 and IPv6 are available and display accordingly
        if (data.ipv4) {
            ip4Element.innerHTML += `IPv4: ${data.ipv4}<br>`;
        }

        // Validate IPv6 address
        if (data.ipv6 && isValidIPv6(data.ipv6)) {
            ip6Element.innerHTML += `IPv6: ${data.ipv6}<br>`;
          }
//        } else if (data.ipv6) {
//            // Fallback if fetched value is not a valid IPv6
//            console.warn(`Received an invalid IPv6 address: ${data.ipv6}`);
//        }

        if (!data.ipv4 && !data.ipv6) {
            ip4Element.innerHTML = 'No IPv4 addresses available.';
            ip6Element.innerHTML = 'No IPv6 addresses available.';
        }
    } catch (error) {
        console.error('Error fetching IP address:', error);
    }
}

// https://stackoverflow.com/questions/46155/how-can-i-validate-an-email-address-in-javascript
// Validate an email with regex.
const validateEmail = (email) => {
    return String(email)
        .toLowerCase()
        .match(
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        );
};

//----------------
// Email encoding/decoding for bots
//----------------

// https://andrewlock.net/simple-obfuscation-of-email-addresses-using-javascript/

function encodeEmail(email) {

    // Dynamically generate a random key instead of a fixed value
    const key = Math.floor(Math.random() * 256);

    // Hex encode the key with a random value
    const encodedKey = key.toString(16).padStart(2, '0'); // Ensure two digits
    let encodedString = encodedKey;

    // loop through every character in the email
    for (let n = 0; n < email.length; n++) {
        // Get the code (in decimal) for the nth character
        const charCode = email.charCodeAt(n);

        // XOR the character with the key
        const encoded = charCode ^ key;

        // Hex encode the result, and append to the output string
        encodedString += make2DigitsLong(encoded.toString(16));
    }
    return encodedString;
}

function make2DigitsLong(value) {
    return value.length === 1
        ? '0' + value
        : value;
}

function decodeEmail(encodedString) {
    // Holds the final output
    var email = "";

    // Extract the first 2 letters
    var keyInHex = encodedString.substr(0, 2);

    // Convert the hex-encoded key into decimal
    var key = parseInt(keyInHex, 16);

    // Loop through the remaining encoded characters in steps of 2
    for (var n = 2; n < encodedString.length; n += 2) {

        // Get the next pair of characters
        var charInHex = encodedString.substr(n, 2)

        // Convert hex to decimal
        var char = parseInt(charInHex, 16);

        // XOR the character with the key to get the original character
        var output = char ^ key;

        // Append the decoded character to the output
        email += String.fromCharCode(output);
    }
    return email;
}

//
// Decode the emails into the browser

// Find all the elements on the page that use class="eml-protected"
var allElements = document.getElementsByClassName("eml-protected");

// Loop through all the elements, and update them
for (var i = 0; i < allElements.length; i++) {
    updateAnchor(allElements[i])
}

function updateAnchor(el) {
    try {
        // fetch the hex-encoded string
        const encoded = el.innerHTML;

        // decode the email, using the decodeEmail() function from before
        const decoded = decodeEmail(encoded);

        // Replace the text (displayed) content
        el.textContent = decoded;

        // Set the link to be a "mailto:" link
        el.href = 'mailto:' + decoded;
    } catch (error) {
        console.error("Error decoding email:", error);
        el.textContent = "Email decoding error!";
        el.href = '';
    }
}


// Get the decoded email from the form box
function getDecodedEmail() {
    let decodedEmail = document.getElementById("decoded_email").value;
    if (validateEmail(decodedEmail)) {
        // let encodedEmail = encodeEmail(decodedEmail, 16);
        let encodedEmail = encodeEmail(decodedEmail);
        // console.log(decodedEmail + " is a valid email.");
        // console.log(encodeEmail(decodedEmail, 16));
        // console.log(encodedEmail);

        // Ohh, I had the damn p tag set to class and not ID, oops...
        let encodedEmailOutput = document.getElementById("encoded_email_output");
        let decodedEmailOutput = document.getElementById("decoded_email_output");


        if (decodedEmail != null) {

            // First toggle the hidden on or off when pressing the button.
            // if (encodedEmailOutput.hasAttribute('hidden') || decodedEmailOutput.hasAttribute('hidden')) {
            //     encodedEmailOutput.removeAttribute('hidden');
            //     decodedEmailOutput.removeAttribute('hidden');
            // } else {
            //     encodedEmailOutput.setAttribute('hidden', "");
            //     decodedEmailOutput.setAttribute('hidden', "");
            // }

            // Encoded email for output
            encodedEmailOutput.innerHTML = "Encoded Email: " + encodedEmail;

            // Decoded email for output
            decodedEmailOutput.innerHTML = "Decoded Email: " + decodeEmail(encodedEmail);
        }
    } else {
        console.log(decodedEmail + " is an invalid email.");
    }
}

//--------
// Showing/hiding tags for checkboxes.

// Uses the checkbox I have setup in the HTML to show/hide the email instead of doing it in the function.
function showHideEmailCheckbox() {
    let checkboxHiddenStatus = document.getElementById("show_or_hide_email_checkbox");
    let encodedEmailOutput = document.getElementById("encoded_email_output");
    let decodedEmailOutput = document.getElementById("decoded_email_output");

    let emailCheckboxText = document.getElementById("email_status");


    if (!checkboxHiddenStatus.checked) {
        encodedEmailOutput.removeAttribute('hidden');
        decodedEmailOutput.removeAttribute('hidden');
        emailCheckboxText.innerHTML = "Shown";
    } else {
        encodedEmailOutput.setAttribute('hidden', '');
        decodedEmailOutput.setAttribute('hidden', '');
        emailCheckboxText.innerHTML = "Hidden";
    }
}

function showHideIp() {
    let ipHiddenStatus = document.getElementById("show_or_hide_ip_checkbox");
//    let ipOutput = document.getElementById("ip");
    const ip4Output = document.getElementById("ipv4");
    const ip6Output = document.getElementById("ipv6");

    let ipCheckboxText = document.getElementById("ip_status");

    if(!ipHiddenStatus.checked) {
//        ipOutput.removeAttribute('hidden');
        ip4Output.removeAttribute('hidden');
        ip6Output.removeAttribute('hidden');
        ipCheckboxText.innerHTML = "Shown";
    } else {
//        ipOutput.setAttribute('hidden', '');
        ip4Output.setAttribute('hidden', '');
        ip6Output.setAttribute('hidden', '');
        ipCheckboxText.innerHTML = "Hidden";
    }
}

function showHideUserAgent() {
    let userAgentHiddenStatus = document.getElementById("show_or_hide_useragent_checkbox");
    let userAgentOutput = document.getElementById("user-agent");
    let userAgentCheckboxText = document.getElementById("user_agent_status");

    if(!userAgentHiddenStatus.checked) {
        userAgentOutput.removeAttribute('hidden');
        userAgentCheckboxText.innerHTML = "Shown";
    } else {
        userAgentOutput.setAttribute('hidden', '');
        userAgentCheckboxText.innerHTML = "Hidden";
    }

}

//----------------

// https://medium.com/@aleksej.gudkov/how-to-detect-the-clients-browser-name-a-practical-guide-b88f10604d3f
// Detect browser test, seems to display what browser the user is using.
function detectBrowser() {
    const userAgent = navigator.userAgent;
    if (userAgent.includes("Firefox")) {
        return "Firefox";
    } else if (userAgent.includes("Chrome") && !userAgent.includes("Edg")) {
        return "Chrome";
    } else if (userAgent.includes("Safari") && !userAgent.includes("Chrome")) {
        return "Safari";
    } else if (userAgent.includes("Edg")) {
        return "Microsoft Edge";
    } else if (userAgent.includes("Opera") || userAgent.includes("OPR")) {
        return "Opera";
    } else if (userAgent.includes("MSIE") || userAgent.includes("Trident")) {
        return "Internet Explorer";
    } else {
        return "Unknown Browser";
    }
}

// Set the user agent string in the HTML
function setUserAgent() {
    let currentUserAgent = navigator.userAgent;
    let userAgentID = document.getElementById("user-agent");

    // if (userAgentID.hasAttribute('hidden')) {
    //     userAgentID.removeAttribute('hidden');
    // } else {
    //     userAgentID.setAttribute('hidden', "");
    // }

    userAgentID.innerHTML = "Current user agent for browser: " + currentUserAgent;
}

