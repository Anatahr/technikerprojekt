<?php

        $Encoded=file_get_contents('php://input');
        $Decoded=json_decode($Encoded,true);
        $APIString=$Decoded["Schluesel"];
        if($APIString=="fdcgDSWcPxNEcYFhm9PAS4mhgzP2HjNqCzvkYX9Y4sPccsP4yH3o8ujQvvYm9ez6Jtyv9abxQxMJfHfRMiLn3r3Pns9EKmCQH9zMtfWVLVAcnrRLQrcfjZPqUhS2HTTJ")
        {
                $CN=mysqli_connect("localhost","applogin","2B@apC6CfUPM9i@T6p#pS6TBd!o25sV7ouEsM2B");
                $DB=mysqli_select_db($CN,"Homesecurity");

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




