// I finally figured this out, I had to use some guides from stack overflow combined with a w3schools page.
// Got working on 2-22-2024 @ 7:17PM

// This might be useful:
// https://dev.to/raaynaldo/an-easy-way-to-understand-promise-in-javascript-215i

// https://stackoverflow.com/questions/21626048/unable-to-pass-jinja2-variables-into-javascript-snippet

$(function() {
    $('#mybutton').on('click', async function(e) {

        // I finally got the password outputting to the console!!!!
        // Combined this answer https://stackoverflow.com/a/12322162 with some other 
        // part from here: https://www.w3schools.com/jquery/tryit.asp?filename=tryjquery_ajax_get
        // This works perfectly for outputting the data to 
        $(document).ready(function() {
        $.ajax({
            url: "/passwordgen",
            type: "GET",
            "dataType": "html",
            success: function(data) {
                document.getElementById('passwordtest').innerHTML = data;
                // console.log(data);
            }
        });
    })}
)});
