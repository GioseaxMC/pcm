<?php

#ifdef DEBUG
error_reporting(E_ALL); ini_set('display_errors', 1); ini_set('display_startup_errors', 1);
#endif

$host = "localhost";
#include "ign.cred.php"
$database = "LabTelecomunicazioni";

$db = new mysqli($host, $username, $password, $database);
$db->options(MYSQLI_OPT_INT_AND_FLOAT_NATIVE, 1);

function q($query) {
    global $db;
    return $db->query($query);
};

?>

<script src="https://code.jquery.com/jquery-4.0.0.min.js"></script>

#include "style.php"

<define> navbtn(page, ...) nav(page, <button class=btn><vargs></button>)

<define> rows style="display: flex; flex-direction: row; gap: 20px; flex: 1"
<define> cols style="display: flex; flex-direction: column; gap: 20px; flex: 1"

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PC Manager</title>
</head>
<body style="display: flex; flex-direction: column">
    <div class=navbar>
        #ifdef DEBUG
        Debug mode
        #endif
        <div rows>
            <div style="display: flex; align-items: center">
                <p>
                    <span class="title">PC Manager</span>
                    <span class="sub">by giuseppe mortara</span>
                </p>
            </div>
            navbtn(pcs, Portatili)
        </div>
    </div>
    <div style="height: 100%; display: flex">
        <div rows>
            <div class=sidebar>
                <div cols>
                    navbtn(classi, Classi)
                </div>
            </div>
            <div class=RouterWrapper>
                <Routers>
            </div>
        </div>
    </div>
</body>
</html>