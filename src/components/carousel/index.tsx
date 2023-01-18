import React from 'react'

const Carousel = () => {
  return (
    <>
    
    <div id="controls-carousel" className="relative" data-carousel="slide">
    
    <div className="relative h-56 overflow-hidden rounded-lg md:h-96">
            <div className="hidden duration-700 ease-in-out" data-carousel-item>
                <img src="https://www.pontotel.com.br/wp-content/uploads/2022/05/imagem-corporativa.jpg" className="absolute block w-full -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2" alt="..."/>
            </div>

            <div className="hidden duration-700 ease-in-out" data-carousel-item>
                <img src="https://www.ufmt.br/ocs/images/phocagallery/galeria2/thumbs/phoca_thumb_l_image03_grd.png" className="absolute block w-full -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2" alt="..."/>
            </div>
        </div>
        
    </div>

    
    </>
  )
}

export default Carousel