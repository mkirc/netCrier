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
					<select name="date" form="dateform">
					  <option selected="selected">Choose date</option>
					  <?php
					    foreach($rows as $date) { ?>
					      <option value="<?php echo $date['scrap_ts'] ?>"><?php echo date('M j Y',strtotime($date['scrap_ts'])) ?></option>
					  <?php
					    } ?>
					</select>
        		</td>
        		<td>
        			<form action="#" id="dateform" method="post">
        				<input type="submit" value="SuperCoolButtonYo">
        			</form>
        		</td>
        	</tr>
        </tbody>
    </table>
</center>

<!-- <?php

    if(isset($_POST))
    {
        echo htmlentities($_POST['date']);
        print_r($_POST);
    }

?> -->

<?php
function getGenByDate($rows) {
	$outarray = array();
	foreach ($rows as $a) {
		// echo $a;
		// print_r($a['scrap_ts']);
		if((string)$a['scrap_ts'] === (string)$_POST['date']) {
			// echo 'yay';
			array_push($outarray, $a);
		}
	}
	return $outarray;
}

?>

<!-- <?php
// echo getGenByDate();
print_r(getGenByDate($rows));
?>
 -->
<center>
    <table class="table table-bordered table-condensed">
        <thead>
            <tr>
                <th>ID</th>
                <th>Text</th>
            </tr>
        </thead>
        <tbody>
			<?php foreach (getGenByDate($rows) as $input): array_map('htmlentities', $input); ?>
			    <tr>
			        <td><?php echo htmlspecialchars($input['gen_id']); ?></td>
			        <td><?php echo htmlspecialchars($input['gen_txt']); ?></td>
			    </tr>
			<?php endforeach; ?>
        </tbody>
    </table>
</center>



<?php include "templates/footer.php"; ?>