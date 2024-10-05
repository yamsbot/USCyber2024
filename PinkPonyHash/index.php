<!DOCTYPE html>

<?php
    $secret = "testing_testing_123";
    assert(strlen($secret) == 19);

    //make a new cookie for the user
    function make_cookie() {
        global $secret;

        $payload = "kitty_cat";
        setcookie("token", base64_encode($payload) . "." . sha1($secret . $payload));
        header("Location: /"); //reload page
        exit(); //we're done
    }

    //if no cookie token, set it
    if(!isset($_COOKIE["token"])) {
        
        echo "no cookie, setting!\n";
        make_cookie();
    }

    //if there is a cookie, parse it
    echo "parsing cookie\n\n";
    $parsed = explode(".", $_COOKIE["token"]);

    //check sanity
    if(count($parsed) !== 2) {
        make_cookie();
    }

    //verify the hash is sane
    //also make sure the payload is base64 encoded
    $payload = base64_decode($parsed[0]);
    $hash = $parsed[1];
    if($payload === false) {
        make_cookie();
    }
    
    if(sha1($secret . $payload) !== $hash) {
        make_cookie();
    }

    //check if we're in the pink pony club
    if(strstr($payload, "pink_pony")) {
        $flag = "FFCTF{Th!\$_iS_4_Fl@g}";
        echo "<h1>OMG A MEMBER OF THE PINK PONY CLUB?! HERES UR FLAG: $flag</h1>";
    }else{
        echo "<h1>sry we only give flags to members of the pink pony club, not $payload :c</h1>";
    }
?>
