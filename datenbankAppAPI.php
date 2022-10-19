<?php

        $Encoded=file_get_contents('php://input');
        $Decoded=json_decode($Encoded,true);
        $APIString=$Decoded["Schluesel"];
        if($APIString=="")
        {
                $CN=mysqli_connect("localhost","Loginname","pw");
                $DB=mysqli_select_db($CN,"datenbank");

                $SQ="SELECT * from Entsperlog ORDER BY Nr DESC LIMIT 10";
                $Table=mysqli_query($CN,$SQ);

                if(mysqli_num_rows($Table)>0)
                {
                        while($Row=mysqli_fetch_assoc($Table))
                        {
                                $Name=$Row["Name"];
                                $Datum=$Row["Datum"];
                                $Zeit=$Row["Zeit"];


                                $Response[]=array(
                                        "Name"=>$Name,
                                        "Datum"=>$Datum,
                                        "Zeit"=>$Zeit
                                );

                        }
                }

                echo json_encode($Response);
        }
?>




