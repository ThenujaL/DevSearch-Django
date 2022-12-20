// Get search form and page links
let searchForm = document.getElementById('searchForm')
let paegeLinks = document.getElementsByClassName('page-link')

if (searchForm){
    for (let i = 0; paegeLinks.length > i; i++){
        paegeLinks[i].addEventListener('click', function (e) {
            e.preventDefault()

            //Getting page njumber from data atribute
            let page = this.dataset.page

            //submit a hidden htmly from with the page number
            searchForm.innerHTML += `<input value=${page} name="page" hidden/>`

            //submit form
            searchForm.submit()
        })
    }
}