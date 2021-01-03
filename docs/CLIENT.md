<h1>How to use (Client)</h1>
    <p><small>All params can be can be lowercase or uppercase.</small></p>
    <table>
      <tr>
        <th>Name</th>
        <th>Details</th>
        <th>Example</th>
      </tr>
      <tr>
        <td>id</td>
        <td>Returns storms by depression ID.</td>
        <td>26L</td>
      </tr>
      <tr>
        <td>name</td>
        <td>Returns storms by international WMO name.</td>
        <td>Delta</td>
      </tr>
      <tr>
        <td>basin</td>
        <td>Returns storms by their respective oceanic basin.</td>
        <td>ATL</td>
      </tr>
        <h2>Responses</h2>
        <p>All responeses will be in JSON format.</p>
        <table>
      <tr>
        <th>Name</th>
        <th>Details</th>
      </tr>
      <tr>
        <td>last-updated</td>
        <td>Date string (HH:MM:SS) of when the API was last updated. (UTC-0)</td>
      </tr>
      <tr>
        <td>storms</td>
        <td>Returns a list of dictionaries for each active storm.</td>
      </tr>
      <tr>
        <td>id</td>
        <td>(Nested in <i>storms</i> response) Depression of an active storm. Contains a dictionary of the values (basin, date, latitude, longitude, name, pressure, time, vmax<sup>1</sup></td>
      </tr>
    </table>
    <p><sup>1. Vmax is the maximum 1-minute sustained winds in knots.</sup><p>
    <img src="images/client_json_response_all.png" title="Default API response" align="center" height=100>
    <p>Example url to get all storms in the Atlantic basin: <a href="http://127.0.0.1:5000/api/?basin=atl" target="_blank">http://127.0.0.1:5000/api/?basin=atl</a></p>
    <p>A live api of all storms can be found at <a href="http://127.0.0.1:5000/api/" target="_blank">http://127.0.0.1:5000/api/</a></p>