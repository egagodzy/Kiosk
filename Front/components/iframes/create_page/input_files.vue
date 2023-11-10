<template>
    <div>
      <div class="flex flex-col items-center w-full mt-5">
        <input type="file" class="flex w-4/5 bg-blue-500" multiple @change="handleFileUploads( $event )"/>
        <p v-if="Error_Input" class="flex text-red-600">
          {{ Error_Input }}
        </p>
      </div>
      <div class="flex flex-wrap">
        <div class="flex flex-col w-1/4 my-5" v-for="file in testG">
          <img class="flex mx-auto h-[100px] w-[100px]" v-if="testG" :src="file.url" />
          <p class="flex mx-auto my-1">{{ file.name }}</p>
        </div>
      </div>
      <button class="flex mt-5 bg-blue-500 h-[50px] hover:bg-blue-700 focus:bg-blue-700 text-white font-bold mx-auto my-auto py-2 px-2 rounded justify-center items-center" v-on:click="submitFiles()">
        <div v-if="data_load === true" class="flex flex-row mr-2 h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]" role="status">
        </div>
        {{ text_load_button }}
      </button>
    </div>
</template>

<script>
import axios from 'axios';
  export default {
    data(){
        return {
            files: '',
            data_load: false,
            text_load_button: "Загрузить",
            Error_Input: '',
            urls: [],
            testG: [],
        }
    },
    methods: {
      handleFileUploads(event){
        this.files = event.target.files;
        for (let i = 0; i < this.files.length; i++) {
          console.log(this.files[i].name);
          this.urls.push(URL.createObjectURL(this.files[i]));
          let Demo = {"name": this.files[i].name, "url": URL.createObjectURL(this.files[i])};
          this.testG.push(Demo);
          
        };
        console.log(this.testG);
        //this.url = URL.createObjectURL(this.files);
      },
      submitFiles(){
        console.log("Это файлы: " + this.files)
        if (this.files === "") {
          console.log("Ошибка");
          this.Error_Input = "Добавьте файлы для загрузки.";
        } else {
          this.Error_Input = "";
          let formData = new FormData();
          this.data_load = true;
          this.text_load_button = "Загрузка...";
          for( var i = 0; i < this.files.length; i++ ){
            let file = this.files[i];
            formData.append("files", file);
          };
          axios.post( 'http://localhost:1337/single-file', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          .then(response => {
            this.data_load = false;
            this.text_load_button = "Загрузить"
            console.log("Успешно " + response.data);
          })
          .catch(error => console.log(error));
        }
      }
    }
  }
</script>