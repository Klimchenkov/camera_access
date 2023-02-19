<script setup>
import { onMounted,ref } from 'vue'

const connection = new WebSocket("ws://localhost:8000/ws");


onMounted(() => {
  connection.onmessage = function(e){
    let image = document.getElementById("frame");
    image.onload = function(){
                URL.revokeObjectURL(this.src); 
            }
    image.src = URL.createObjectURL(e.data);
  };
})

</script>

<template>
  <img id="frame" src="">
</template> 