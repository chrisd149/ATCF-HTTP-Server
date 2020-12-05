<h1>How to use (Client)</h1>
    <p><small>All params can be can be lowercase or uppercase.</small></p>
    <h4>/api/</h4>
    <p>Returns all storms' data in JSON format.</p>
    <h4>id</h4>
    <p>Returns storm by depression id (i.e. 12L.)</p>
    <h4>name</h4>
    <p>Returns storm by name (i.e. Iota.)</p>
    <h4>basin</h4>
    <p>Returns all storms in a basin (i.e. ATL.)</p>
    <p><small>Make sure to add <i>args?</i> to the end of <i>/api/</i> for id, name, or basin.</small></p>
        <h2>Responses</h2>
        <hr>
        <table>
      <tr>
        <th>Name</th>
        <th>Details</th>
      </tr>
      <tr>
        <td>last-updated</td>
        <td>Date string (HH:MM:SS) of when the API was last updated.</td>
      </tr>
      <tr>
        <td>storms</td>
        <td>Returns a list of dictionaries for each active storm.</td>
      </tr>
      <tr>
      <tr>
        <td>id</td>
        <td>(Nested in <i>storms</i> response) Depression of an active storm. Contains a dictionary of the values (basin, date, latitude, longitude, name, pressure, time, vmax).</td>
      </tr>
    </table>
    <p>Example url to get all storms in the Atlantic basin: <a href="http://127.0.0.1:5000/api/args?basin=atl">(http://127.0.0.1:5000/api/args?basin=atl)</a></p>
    <p>A live api of all storms can be found at <a href="http://127.0.0.1:5000/api">http://127.0.0.1:5000/api</a>/</p>
    <footer><small>Contact: <a href="mailto:christianmigueldiaz@gmail.com">christianmigueldiaz@gmail.com</a></small></footer>