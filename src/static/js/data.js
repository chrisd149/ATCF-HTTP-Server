// Coverts data/data.csv to an HTML table to be returned
// Note: I have never coded in JS
function arrayToTable(tableData) {
    var table = $('<table></table>');
    $(tableData).each(function (i, rowData) {
        var row = $('<tr></tr>');
        $(rowData).each(function (j, cellData) {
            row.append($('<td>'+cellData+'</td>'));
                    });
                table.append(row);
                });
                return table;
            }

$.ajax({
    type: "GET",
    url: "data/data.csv",
    success: function (data) {
        $('body').append(arrayToTable(Papa.parse(data).data));
            }
        });