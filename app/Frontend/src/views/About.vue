<script setup>
import { onMounted, ref } from 'vue';
import { gsap } from 'gsap';
import logo1 from '@/assets/p1.png';
import logo2 from '@/assets/p2.png';
import logo3 from '@/assets/p3.png';

import pp0 from '@/assets/p0.jpeg';
import pp1 from '@/assets/pp1.jpg';
import pp2 from '@/assets/pp2.jpg';
import pp3 from '@/assets/pp3.jpg';

import conf from '@/assets/conf.gif';

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

    if (isMobile_()) {
    // insert into style tag
    const style = document.createElement('style');
    style.innerHTML = `
        .abt1 {
            position: fixed !important;
            top: 50% !important;
            left: 50% !important;
            width: 99vw !important;
            height: 100% !important;
            transform: translate(-50%, -50%) rotate(-4deg) scale(2.1) !important;
            overflow: clip !important;
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: wrap !important;
            align-content: center !important;
            justify-content: center !important;
            align-items: center !important;
            animation: scale 10s infinite alternate !important;
        }

        @keyframes scale {
            0% {
                transform: translate(-50%, -50%) rotate(4deg) scale(2.1) !important;
            }

            50% {
                transform: translate(-50%, -50%) rotate(0deg) scale(2.2) !important;
            }
        }

        .confeti {
            /* display: none !important; */
        }

        .sonf_msg {
            font-size: 7vw !important;
            margin: 0 !important;
        }

        #scene {
            margin-top: 40vh !important;
            width: 65vw !important;
            height: 30vw !important;
            margin-bottom: 45vw !important;
        }

        .title {
            font-size: 10vw !important;
            transform: none !important;
            text-align: center !important;
            padding: 0 !important;
            margin-bottom: 8vw !important;
        }

        .section {
            margin: 2vw 8vw !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            margin-bottom: 10vw !important;
        }

        .description * {
            font-size: 4vw !important;
            font-weight: 400 !important;
            text-align: justify !important;
        }

        .prof {
            width: 100vw !important;
            flex-wrap: nowrap !important;
            gap: 0vw !important;
            margin-top: 0 !important;
            transform: none !important;
            display: flex !important;
            justify-content: center !important;
            flex-direction: column !important;
            align-content: center !important;
            align-items: center !important;
            padding: 0 !important;
            margin: 0 !important;
            gap: 0 !important;
            padding-top: 12vw !important;
        }

        .profcon {
width: 45vw !important;
    padding: 7vw 12vw !important;
    border-radius: 3vw !important;
    border: 0.2vw solid #2035323d !important;
    transform: scale(0.8) !important;
    margin: 0 !important;
        }

        .profcon img {
            filter: grayscale(0) brightness(1) !important;
            width: 45vw !important;
            border-color: teal !important;
        }

        .profname {
            font-size: 6.5vw !important;
            color: rgb(0, 42, 42) !important;
        }

        .profdesc {
            font-size: 2.8vw !important;
        }

        .profcon:active {
            background-color: var(--wl) !important;
            color: white !important;
            box-shadow: 0 0 0 0.5vw var(--wl) !important; 
        }

        .techlis {
            display: flex !important;
            flex-direction: row !important;
            margin: 0 !important;
            padding: 0 !important;
            justify-content: space-evenly !important;
            flex-wrap: wrap !important;
            align-items: stretch !important;
            align-content: center !important;
            gap: 8vw !important;
        }

        .techlis ul {
            display: none !important;
        }

        hv {
            font-size: 3vw !important;
/*            margin-top: 21vw !important;*/
        }

        .thanks {
            margin: 3vw !important;
            font-size: 4vw !important;
            margin-top: 10vw !important;
        }

        .logotape {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            gap: 9vw !important;
            flex-direction: column !important;
            flex-wrap: nowrap !important;
            align-content: center !important;
            margin-top: 21vw !important;
        }

        .logotape img {
            height: 3vw !important;
        }

        .emdcredd {
            margin-top: 10vw !important;
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-content: center !important;
            justify-content: center !important;
            transform: scale(0.7) !important;
        }

        .foot {
            display: flex !important;
            font-size: 4vw !important;
            gap: 4vw !important;
        }

        .nulllfont {
            font-size: 6vw !important;
        }
    `;
    document.head.appendChild(style);
}


    setInterval(changeImage, 4000);
    setInterval(() => {
    
        // change opacuty of the confeti to 0 and after 1 second display none
        document.querySelector('.confeti').style.opacity = 0;
        setTimeout(() => {
            document.querySelector('.confeti').style.display = 'none';

        }, 1000);
    }, 4000);
});

const isMobile_ = () => {
  return /Android|webOS|iPhone|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
};

console.log(isMobile_());


const looper = 800;
</script>

<template>
    <div class="confeti">
        <img class="cnfff" :src=conf alt="Avatar" style="width: 100vw; height: 100vh;">
        <div class="sonf_msg">🏆</div>
    </div>
    <canvas id="scene"></canvas>
    <div class="abt1">
        <p v-for="(text, index) in Array(looper).fill(['Google', 'Worldline', 'Nullbyte']).flat()" :key="index">{{ text }}</p>
    </div>


    <div class="section">
        <div class="title "
        >About Us</div>
        <div class="description ">
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
        <div class="description ">
            <p>
               Started as a team of four developers, we have been working together on some pretty cool projects &
            </p>

            <p>
                We decided to take part in the Worldline Google Cloud 2024 Hackathon.
            </p>
        </div>


        <div class="prof ">
        <a class="profcon" target="_blank" href="https://www.linkedin.com/in/jesvijonathan/">

                <img :src=pp0 alt="Avatar" style="width:100%">
                <div class="profname">Jesvi Jonathan</div>
                <div class="profdesc">
                    <p>Worldline > MS > WLPFO</p>
                    <p>Software Engineer</p><br>
                    <p class="tops">THE HARDCODER ⚡</p>
                </div>
            </a>
            <a class="profcon" target="_blank" href="https://www.linkedin.com/in/akileswar/">

                <img :src=pp1 alt="Avatar" style="width:100%">
                <div class="profname">Akileswar PrathapKumar  </div>
                <div class="profdesc">
                    <p>Worldline > MS > WLPFO</p>
                    <p>Software Engineer</p><br>
                    <p class="tops">THE DEPLOYER 👨‍💻</p>
                </div>
            </a>
            <a class="profcon" target="_blank" href="https://www.linkedin.com/in/rashmi2001/">

                <img :src=pp3 alt="Avatar" style="width:100%">
                <div class="profname">Rashmi Abdulrahim</div>
                <div class="profdesc">
                    <p>Worldline > MS > WLPFO</p>
                    <p>Associate Engineer </p><br>
                    <p class="tops">THE SKIBIDI 👨🏿</p>
                </div>
            </a>
            <a class="profcon" target="_blank" href="https://www.linkedin.com/in/rajashree-g-d-5907821b1/">

                <img :src=pp2 alt="Avatar" style="width:100%">
                <div class="profname">Rajashree Dinakaran</div>
                <div class="profdesc">
                    <p>Worldline > MS > WLPFO</p>
                    <p>Associate Engineer</p>
                    <br>
                    <p class="tops">THE NARRATOR 🎤 </p>
                </div>
            </a>


        </div>

    </div>



    <div class="section">
        <div class="title ">The Making</div>
<div class="imgdes">
    <div class="description ">
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
        <div class="title ">Techstack</div>
        <div class="description ">
            <!-- TECH STACK : PYTHON , VUE JS , MYSQL,  Multimodal Models ,Compute Engine , Cloud GPU , Cloud SQL ,  -->
<!-- Cloud Run , Cloud Storage ,Ollama,ACTIVE DIRECTORY. -->
            <p>
            We have incorporated all the latest tech stack for this project of ours to come up with the best outcome. For more information check the projects <a style="text-decoration: underline;" target="_blank" href="https://github.com/jesvijonathan/Nullbyte-Ticketing-System">Github Repo</a></p>

<div class="techlis">
    <ul>
            <li>Vue 3</li>
            <li>PYTHON</li>
            <li>MYSQL</li>
            <li>Linux</li>
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
.sonf_msg {
    display: flex;
    z-index: 100;
    justify-content: center;
    font-size: 2.8vw;
    font-weight: 500;
    font-family: "Jersey 10", sans-serif;
    text-align: center;
    color: rgba(0, 0, 0, 1);
    padding: 1vw;
    position: absolute;
    top: 70%;
    left: 50%;
    margin-left: 1vw;
    transform: translate(-50%, -50%);
    animation: scale 5s infinite alternate;
}

@keyframes scale {
    0% {
        transform: translate(-50%, -50%) rotate(4deg) scale(1.1);
        color: rgba(0, 0, 0, 0.5);
    }
    50% {
        transform: translate(-50%, -50%) rotate(0deg) scale(1.2);
        color: rgba(0, 0, 0, 0.8);
    }
}
.confeti{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 100;
    transition: 0.5s;
}
.tops{
    font-weight: 900;
    font-family: wl2;
}
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
    gap: 2vw;
    flex-direction: row;
    align-content: space-between;
    justify-content: space-between;
    align-items: center;
    margin-top: 0vw;
    width: 60vw;
    transform: scale(0.9) translateX(6vw);
}

.prof_left{
    width: initial;
    transform: scale(0.9);
    gap: 4vw;
    margin-top: 2vw;
}

.profcon {
    margin-top: 3vw;
    width: 10vw;
    cursor: pointer;
    /* overflow: clip; */
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    align-items: center;
}

.profcon img {
    border-radius: 0.6vw;
    width: 100%;
    transition: filter 0.2s, transform 0.2s;
    filter: grayscale(0.4) brightness(1);
    border: 0.2vw solid rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    image-rendering: pixelated;
    image-rendering: crisp-edges;
    image-rendering: auto;
}

.profcon:hover .profname {
    text-decoration: underline;
}

.profcon:hover img {
    filter: grayscale(0) brightness(1.1);
    transform: scale(1.05);
}



.profname {
    font-size: 1.4vw;
    font-weight: 500;
    font-family: "Jersey 10", sans-serif;
    text-align: center;
    color: black;
    font-style: oblique;
    padding-top: 0vw;
    opacity: 0.7;
    text-wrap: nowrap;
    padding-bottom: 0.6vw;
    margin-top: 1vw;
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



  .cnfff{
        opacity: 0.5;
    }
</style>
