<?php
    if(isset($_POST['name']) && isset($_POST['email']) && isset($_POST['message'])){
        $to = 'georgyim@gmail.com'; 
        $subject = 'Новое сообщение с сайта'; 
        $headers = 'From: ' . $_POST['email'] . "\r\n"; 
        $message = 'Имя: ' . $_POST['name'] . "\n" . 'Сообщение: ' . $_POST['message'];

        if(mail($to, $subject, $message, $headers)) {
            echo 'Сообщение отправлено. Спасибо за обращение!';
        } else {
            echo 'Ошибка отправки. Пожалуйста, попробуйте еще раз.';
        }
    } else {
        echo 'Ошибка: не все поля были заполнены.';
    }
?>