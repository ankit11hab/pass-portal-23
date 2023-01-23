const addIndividual = document.querySelector(".addIndividualBtnDiv");
const referenceDiv = document.querySelector(".form-bottom");
let k = 0;
// const number_arr=["Second","Third","Fourth","Fifth","Sixth","Seventh","eighth","ninth","eleventh"];
const removeButton = document.querySelector("#removeBtn-1");

addIndividual.addEventListener("click", (target) => {
  console.log("hi");
  referenceDiv.insertAdjacentHTML(
    "beforebegin",
    `<div class="form-mid" id="extraDiv${k + 1}">
    <!-- <img class="bgpic" src="./form mid.png" alt=""> -->
    <div class="form">
        <div class="person">
            <div class="pass-type">
                <P class="p-person"> Member</P>
                <div class="remove-button" id="removeBtn-${
                  k + 1
                }" onclick="Delete(event, 'extraDiv${k + 1}')">
                    Remove
                </div>
                <p class="textinput">Pass type</p>
                <div class="custom-select">
                    <select name="pass_type" id="" onchange=onchnge_()>
                    <option value="exclusive"> Exclusive
                    </option>
                </select>
                </div>
            </div>
            <div class=" pass-type">
                <p class="textinput"> First Name</p>
                <input type="text" class="input-text-field " name="first_name" required>
            </div>
            <div class=" pass-type">
                <p class="textinput"> Last Name</p>
                <input type="text" class="input-text-field " name="last_name" required>
            </div>
            <div class="pass-type">
                <p class="textinput">E-mail</p>
                <input type="text" class="input-text-field " name="email" required>
            </div>
            <div class=" pass-type">
                <p class="textinput">Phone Number</p>
                <input type="number" class="input-text-field " name="contact_no" required>
            </div>
            <div class=" pass-type">
                <p class="textinput">ID Type</p>
                <select name="IDtype" id="" class="input-text-field">
                  <option value="none" disabled selected hidden>Select</option>
                  <option value="collegeID"> CollegeID
                  </option>
                  <option value="aadhar"> Aadhar
                  </option>
                  <option value="voterid"> Voter ID
                  </option>
                  <option value="drivinglicense"> Driving License
                  </option>
                  <option value="other"> Other
                  </option>
                </select>
              </div>
              <div class=" pass-type">
                <p class="textinput">ID Number</p>
                <input required type="text" name="IDnumber" class="input-text-field"/>
              </div>
            <div class="pass-type age-gen">
                <div class="pass-gender">
                    <p class="textinput">Gender</p>
                    <div class="custom-select2">
                        <select name="gender" id="">
                        <option value="" disabled selected hidden ></option>
  
                    <option value="male"> Male
                    </option>
                    <option value="female"> Female
                    </option>
                    <option value="other"> Rather don't say
                    </option>
                    </select>
                    </div>
                </div>
                <div class="pass-age">
                    <p class="textinput">Age</p>
                    <div class="custom-select3">
                <input class="input-text-field" type='number' name='age'>
                    </div>
                </div>
            </div>

        </div>
        
    </div>
</div>`
  );
  k++;
  onchnge_();
});

// removeButton.addEventListener('click',target=>{
//     console.log("remove");
//     const extraDivision=document.querySelector("#extraDiv1");
//     extraDivision.innerHTML=``;
// });
function Delete(event, id) {
  onchnge_();
  event.preventDefault();
  var element = document.getElementById(id);
  element.parentNode.removeChild(element);
}
