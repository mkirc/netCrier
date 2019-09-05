<?php include "templates/header.php" ?>
<?php 
require "config.php";

$conn = mysqli_connect($config['host'], $config['user'], $config['pw'], $config['dbname']);
//Check connection
if (mysqli_connect_errno()){
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
$result = mysqli_query($conn, "SELECT * FROM gen ORDER BY gen_id desc LIMIT 10");

//Fetch all records
$rows = mysqli_fetch_all($result,MYSQLI_ASSOC);
// print_r($rows);

//Free result set
mysqli_free_result($result);
mysqli_close($con);
?>
<center>
    <table class="table table-bordered table-condensed">
        <thead>
            <tr>
                <th>Number</th>
                <th>Text</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($rows as $input): array_map('htmlentities', $input); ?>
                <tr>
                    <td><?php echo htmlspecialchars($input['gen_id']); ?></td>
                    <td><?php echo htmlspecialchars($input['gen_txt']); ?></td>
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
</center>




<?php include "templates/footer.php"; ?>