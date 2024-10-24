<script setup>
import { onMounted } from 'vue';
import { gsap } from 'gsap';
import logo1 from '@/assets/p1.png';
import logo2 from '@/assets/p2.png';
import logo3 from '@/assets/p3.png';

const images = [logo1, logo2, logo3];
let currentImageIndex = 0;
const png = new Image();
png.crossOrigin = "anonymous";
png.src = images[0];

let canvas, ctx, particles = [];
let animationComplete = false;
let imageData;
let isPaused = false;
let mousePosition = { x: 0, y: 0 };

const drawScene = () => {
    particles = [];
    canvas.width = png.width * 6;
    canvas.height = 160;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(png, 0, 0);
    imageData = ctx.getImageData(0, 0, png.width, png.height);

    for (let y = 0; y < imageData.height; y++) {
        for (let x = 0; x < imageData.width; x++) {
            if (imageData.data[(y * 4 * imageData.width) + (x * 4) + 3] > 128) {
                const particle = {
                    x0: x,
                    y0: y,
                    x1: png.width / 1,
                    y1: png.height / 1,
                    speed: Math.random() * 0.7 + 0.7,
                    color: `rgba(${imageData.data[(y * 4 * imageData.width) + (x * 4)]}, ${imageData.data[(y * 4 * imageData.width) + (x * 4) + 1]}, ${imageData.data[(y * 4 * imageData.width) + (x * 4) + 2]}, ${imageData.data[(y * 4 * imageData.width) + (x * 4) + 3]})`
                };

                gsap.to(particle, {
                    duration: particle.speed,
                    x1: particle.x0 * 6,
                    y1: particle.y0 * 6,
                    delay: y / 30,
                    ease: "elastic.out(1, 0.5)",
                    onComplete: () => {
                        if (animationComplete && particles.every(p => p.x1 === particle.x0 * 6 && p.y1 === particle.y0 * 6)) {
                            // Additional logic if needed
                        }
                    }
                });

                particles.push(particle);
            }
        }
    }

    requestAnimationFrame(render);
};

const render = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (const particle of particles) {
        ctx.fillStyle = particle.color;
        ctx.fillRect(particle.x1, particle.y1, 7, 7);

        if (isPaused) {
            const dx = particle.x1 - mousePosition.x;
            const dy = particle.y1 - mousePosition.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            const disperseRadius = 50;

            if (distance < disperseRadius) {
                const force = 0.8;
                const normalizedDx = dx / distance;
                const normalizedDy = dy / distance;
                particle.x1 += normalizedDx * force;
                particle.y1 += normalizedDy * force;
            }
        }
    }
    requestAnimationFrame(render);
};

const changeImage = () => {
    currentImageIndex = (currentImageIndex + 1) % images.length;
    png.src = images[currentImageIndex];
    animationComplete = false;

    png.onload = () => {
        drawScene();
    };
};

onMounted(() => {
    canvas = document.getElementById("scene");
    ctx = canvas.getContext("2d");

    png.onload = () => {
        drawScene();
        canvas.addEventListener('click', () => {
            animationComplete = true;
            drawScene();
        });

        window.addEventListener('mousemove', (event) => {
            mousePosition.x = event.clientX - canvas.getBoundingClientRect().left;
            mousePosition.y = event.clientY - canvas.getBoundingClientRect().top;
        });

        canvas.addEventListener('mouseenter', () => {
            isPaused = true;
        });

        canvas.addEventListener('mouseleave', () => {
            isPaused = false;
        });
    };

    setInterval(changeImage, 4000);
});


const looper = 800;
</script>

<template>
    <canvas id="scene"></canvas>
    <div class="abt1">
        <p v-for="(text, index) in Array(looper).fill(['Google', 'Worldline', 'Nullbyte']).flat()" :key="index">{{ text }}</p>
    </div>


    <div class="section">
        <div class="title jos">About Us</div>
        <div class="description">
            <p>
               We’re a group of four developers working together at Worldline Global Services on some pretty cool projects. 
               Our team includes Jesvi Jonathan, Akileswar Prathapkumar,  Rashmi Abdulrahim, and Rajashree Dinakaran. 
               We bring different strengths to the table, and together, we handle everything from coding to problem-solving. </p>
            <p> Whether it’s tackling tricky bugs, optimizing systems, or coming up with new features, we work together to get things done. 
               Each of us plays a unique role, but it’s our teamwork that really makes things happen. 
               We’re always learning, growing, and pushing the boundaries of what we can do as a team."</p>
        </div>
    </div>


    <div class="section">
        <div class="title ">The Team</div>
        <div class="description jos">
            <p>
               Started as a team of four developers, we have been working together on some pretty cool projects.
            </p>

            <p>
                We took part in the Google Cloud Next 2021 Hackathon.
            </p>
        </div>


        <div class="prof">

            <div class="profcon">

                <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="width:100%">
                <div class="profname">Jesvi Jonathan</div>
                <div class="profdesc">
                    <p>WGS > MS > WLPFO > MARCOPOLO</p>
                    <p>Trainee Engineer</p>
                    <p>Musician & loves to code</p>
                </div>
            </div>
            <div class="profcon">

                <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="width:100%">
                <div class="profname">Akileswar PrathapKumar  </div>
                <div class="profdesc">
                    <p>WGS > MS > WLPFO > MARCOPOLO</p>
                    <p>Trainee Engineer</p>
                    <p>Cofee & Code</p>
                </div>
            </div>
            <div class="profcon">

                <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="width:100%">
                <div class="profname">Rashmi Abdulrahim</div>
                <div class="profdesc">
                    <p>WGS > MS > WLPFO > MARCOPOLO</p>
                    <p>Associate Engineer </p>
                    <p>Docker4Life</p>
                </div>
            </div>
            <div class="profcon">

                <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="width:100%">
                <div class="profname">Rajashree Dinakaran</div>
                <div class="profdesc">
                    <p>WGS > MS > WLPFO > MARCOPOLO</p>
                    <p>Associate Engineer</p>
                    <p>Architect Pro Max</p>
                </div>
            </div>


        </div>

    </div>



    <div class="section">
        <div class="title">The Making</div>
<div class="imgdes">
    <div class="description jos">
    <p>
        Our NullByte Triaging System uses Generative AI and automation to streamline ticket management and improve service efficiency. 
        Users submit queries via LLM-based chat, email, or a portal, which are triaged by a Google Cloud AI-powered model. 
    </p>
    <br>
    <p>
        Integrated with tools like JIRA, PagerDuty, and Serviceline, it offers a unified ticketing experience. 
        The solution is scalable, with automated triggers, Active Directory, and Gen-AI capabilities for optimal performance and reliability.
        Leverage machine learning with Cloud GPUs to process complex inputs like text  images and documents to analyse queries in a natural way.
    </p> 
    <br><p>
        With the help of AI ,we can automatically assign and respond to tickets,  boosting productivity and improving its categorization accuracy over time, 
        all in a single click Created a powerful skill-based routing system that links the tickets to employees based on their knowledge and previous performance.
    </p> 
        </div>
        
        
        <img src="@/assets/code2.jpg" alt="Avatar">
        <img src="@/assets/work.jpg" alt="Avatar" style="">
        
</div>

    </div>

    <div class="section">
        <div class="title">Techstack</div>
        <div class="description jos">
            <!-- TECH STACK : PYTHON , VUE JS , MYSQL,  Multimodal Models ,Compute Engine , Cloud GPU , Cloud SQL ,  -->
<!-- Cloud Run , Cloud Storage ,Ollama,ACTIVE DIRECTORY. -->
            <p>
            We have incorporated all the latest tech stack for this project of ours to come up with the best outcome.</p>

<div class="techlis">
    <ul>
            <li>Vue 3</li>
            <li>PYTHON</li>
            <li>MYSQL</li>
          </ul>
          
    <ul>
            <li>Multimodal Models</li>
            <li>Compute Engine</li>
            <li>Cloud GPU</li>
          </ul>

          <ul>
            <li>Cloud SQL</li>
            <li>Cloud Run</li>
            <li>ACTIVE DIRECTORY</li>
          </ul>

          <ul>
            <li>Ollama</li>
            <li>Vertex API</li>
            <li>GCS Bucket</li>
          </ul>
          <ul>
            <li>Many More..</li>
          </ul>
          </div>

          </div>
    </div>

    <hv>________________________________________________</hv>

<div class="thanks">
    Special Thanks to the organizers and all the people who made this event possible.
</div>


<hv style="margin-top: 3vw;margin-bottom: 4vw;">________________________________________________</hv>

    <div class="logotape">
        
        
        <img src="@/assets/Google_2015_logo.svg.webp" alt="Avatar" style="height: 1.5vw;">

        <img src="@/assets/logo.png" alt="Avatar" style="height: 1vw;">
        
        <img src="@/assets/Nullbyte.svg" alt="Avatar" style="height: 1.2vw;">
    </div>


    <div class="emdcredd">
        <div class="foot">Made with ❤️ by Team <div class="nulllfont">Nullbyte</div></div>

    </div>

    <br><br><br><br><br>
</template>

<style scoped>
hv{
    height: 0.2vw;
    text-align: center;
    position: relative;
    width: 100vw;
    font-size: 0.8vw;
    display: block;
    margin-top: 5vw;
    color: rgba(128, 128, 128, 0.3);
}
.thanks{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 3vw;
    flex-direction: row;
    flex-wrap: nowrap;
    font-size: 1.5vw;
    font-weight: 500;
    font-family: "Jersey 10", sans-serif;
    text-align: center;
    color: rgba(0, 0, 0, 0.8);
    padding: 1vw;
    padding-top: 3vw;
    opacity: 0.7;
    /* padding-top: 4vw; */
}
.logotape{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 4vw;
    margin-top: 5vw;
    flex-direction: row;
    flex-wrap: nowrap;
    /* background-color: rgb(255, 255, 255); */


}
.foot{
    display: flex;
    gap: 1vw;
    justify-content: center;
    align-items: baseline;
    margin-top: 5vw;
    flex-direction: row;
    flex-wrap: nowrap;

}
.foot .nullfont{
    font-size: 2vw;
}
.techlis{
    display: flex;
    margin: 2vw;
    gap: 4vw;
    padding-left: 3vw;
}
.imgdes{
    display: flex;
}
.imgdes img{
    display: none;
    width:10vw; 
    height:17vw;
    margin-left: -8vw;
    transform: translate(90%,-10%) rotate(20deg) scale(0.9);
    filter: grayscale(0.7);
    border-radius: 0.5vw;
    transition: 0.5s;
    z-index: 10
}
.imgdes img:hover{
    transform: translate(90%,0%) rotate(0deg) scale(1.4);
    filter: grayscale(0);
    z-index: 100;
}
.prof {
    display: flex;
    flex-wrap: nowrap;
    justify-content: center;
    gap: 1vw;
}

.profcon {
    margin-top: 5vw;
    height: 20vw;
    width: 12vw;
    cursor: pointer;
}

.profcon:hover {
    filter: brightness(1.1);
}

.profcon img {
    border-radius: 0.3vw
}

.profname {
    font-size: 1.4vw;
    font-weight: 200;
    font-family: "Jersey 10", sans-serif;
    text-align: center;
    color: black;
    padding: 1vw;
    padding-top: 0vw;
    opacity: 0.7;
    text-wrap: nowrap;
    /* padding-top: 4vw; */
}

.profdesc {
    font-size: 0.55vw;
    font-weight: 500;
    font-family: "Jersey 10", sans-serif;
    text-align: center;
    text-align: center;
    color: black;
    padding: 1vw;
    padding-top: 0vw;
    opacity: 0.7;
    /* padding-top: 4vw; */
}

.profdesc p {
    margin: 0;
    padding: 0;
    text-align: center;
}

.section {
    /* border: 2px solid black; */
    margin: 2vw 15vw;
    margin-top: 5vw;

}

.title {
    font-size: 3.5vw;
    font-weight: 900;
    font-family: "Jersey 10", sans-serif;
    text-align: left;
    background-color: white;
    color: teal;
    padding: 1vw;
    text-align: right;
    transform: rotate(-14deg);
    padding-right: 5vw;
    padding-left: 0vw;
    background-color: transparent;
    width: fit-content;
    float: left;
    margin-bottom: 3vw;
    /* margin-right: 2vw; */
}

.description {
    font-weight: 500;
    font-family: "Jersey 10", sans-serif;
    text-align: left;
    color: black;
    padding: 1vw;
    padding-top: 0vw;
    opacity: 0.7;
    /* padding-top: 4vw; */
}

.description * {
    font-size: 1.3vw;
    font-weight: 500;
    font-family: "Jersey 10", sans-serif;
    text-align: left;
    color: black;
    /* font-style: oblique; */
}

.titlel {
    text-align: right;
    transform: rotate(14deg);
    background-color: transparent;
    width: fit-content;
    float: right;
    padding-right: 1vw;
    padding-left: 2vw;
}

body,
html {
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: black;
}

canvas {
    position: relative;
    margin-top: 15vw;
    left: 50%;
    transform: translate(-50%, 0%);
    z-index: 100;
    margin-bottom: 5vw;
}

.abt1 {
    position: fixed;
    top: 50%;
    left: 50%;
    width: 99vw;
    height: 100%;
    transform: translate(-50%, -50%) rotate(-4deg) scale(1.1);
    overflow: clip;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    align-content: center;
    justify-content: center;
    align-items: center;
    animation: scale 10s infinite alternate;
}

@keyframes scale {
    0% {
        transform: translate(-50%, -50%) rotate(4deg) scale(1.1);
    }

    50% {
        transform: translate(-50%, -50%) rotate(0deg) scale(1.2);
    }
}

.abt1 * {

    font-family: "Jersey 10", sans-serif;
    font-weight: 900;
    font-style: normal;
    font-size: 2vw;
    /* color: var(--wl); */
    color: grey;
    opacity: 0.08;
    user-select: none;
    display: flex;
    gap: 0;
}

.abt1 p {
    text-align: center;
    margin: 0;
    padding: 0;
    height: 1vw;
}

/* .abt1 p:hover{
    opacity: 0.6;
     color: var(--wl); 
  } */
</style>