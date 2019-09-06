<?php include "templates/header.php"; ?>


<?php 
require "config.php";

$conn = mysqli_connect($config['host'], $config['user'], $config['pw'], $config['dbname']);
//Check connection
if (mysqli_connect_errno()){
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
$result = mysqli_query($conn, "SELECT s.scrap_ts, g.gen_id, g.gen_txt, g.gen_rating 
	FROM scrap s INNER JOIN gen g ON g.scrap_id = s.scrap_id
	ORDER BY scrap_ts DESC;");

//Fetch all records
$rows = mysqli_fetch_all($result,MYSQLI_ASSOC);
// print_r($rows);

//Free result set
mysqli_free_result($result);
mysqli_close($con);
?>




<center>
    <table class="table table-bordered table-condensed">
        <tbody>
        	<tr>
        		<td>
					<select name="date">
					  <option selected="selected">Choose date</option>
					  <?php
					    foreach($rows as $date) { ?>
					      <option value="<?php echo date('M j Y',strtotime($date['scrap_ts'])) ?>"><?php echo date('M j Y',strtotime($date['scrap_ts'])) ?></option>
					  <?php
					    } ?>
					</select>
        		</td>
        	</tr>
        </tbody>
    </table>
</center>


<?php include "templates/footer.php"; ?>