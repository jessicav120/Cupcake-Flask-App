const BASE_URL = "http://127.0.0.1:5000/api"

function cupcakeHTML(cupcake){
    return `
    <div id=${cupcake.id}>
        <li>
            <h3 style="display:inline-block">${cupcake.flavor} | rating: ${cupcake.rating} | size: ${cupcake.size}</h3>
            <button class='delete' style='margin: 5px'>X</button>
        </li>
        <img src=${cupcake.image} alt="cupcake image">
    </div>
            `
}

async function getCupcakeList(){
    try{
        // get cupcakes from API
        const res = await axios.get(`${BASE_URL}/cupcakes`);
        let cupcakes = res.data.cupcakes;

        // generate HTML for every cupcake
        for (let cpck of cupcakes){
            let cupcake = $(cupcakeHTML(cpck));
            $('#cupcakes').append(cupcake);
        }
    }
    catch {
        error("Something went wrong");
    }
}

//Handle form submit
async function handleAddCupcake(e){
    try{
        e.preventDefault();

        let flavor = $("#flavor").val();
        let size = $("#size").val();
        let rating = $("#rating").val();
        let image = $("#image").val();
    
        const newCupcakeRes = await axios.post(`${BASE_URL}/cupcakes`, {
            flavor: flavor,
            size: size,
            rating: rating,
            image: image
        });
    
        let newCupcake = cupcakeHTML(newCupcakeRes.data.cupcake);
        $('#cupcakes').append(newCupcake);
        $('#add-cupcake-form').trigger("reset");
    } catch {
        err("Something went wrong");
    }
}
$("#add-cupcake-form").on('submit', handleAddCupcake)

//Handle Cupcake Delete
async function deleteCupcake(e){
    try{
        e.preventDefault();

        let $cupcake = $(e.target).closest("div");
        let cupcakeId = $cupcake.attr("id");
    
        await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
        $cupcake.remove();
    } catch {
        err("Something went wrong");
    }
}
$("#cupcakes").on("click", ".delete", deleteCupcake)

//Show current cupcake list on DOM load
$(getCupcakeList);