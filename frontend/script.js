const menuItems = [
    { name: 'Pizza', price: 8.00 },
    { name: 'Cheeseburger', price: 6.50 },
    { name: 'Caesar Salad', price: 6.00 },
    { name: 'Chicken Alfredo Pasta', price: 12.00 },
    { name: 'Fish Tacos', price: 8.00 },
    { name: 'Vegetable Stir-fry', price: 9.50 },
    { name: 'Beef Burrito', price: 8.50 },
    { name: 'Grilled Cheese Sandwich', price: 5.00 },
    { name: 'Chocolate Brownie', price: 3.50 }
];

const menuList = document.getElementById('menu-list');

menuItems.forEach(item => {
    const listItem = document.createElement('li');

    const img = document.createElement('img');
    img.src = `images/${item.name.toLowerCase().replace(/ /g, '-')}.jpg`; 
    img.alt = item.name;

    const detailsDiv = document.createElement('div');
    detailsDiv.className = 'menu-item-details';

    const nameSpan = document.createElement('span');
    nameSpan.className = 'menu-item-name';
    nameSpan.textContent = item.name;

    const priceSpan = document.createElement('span');
    priceSpan.className = 'menu-item-price';
    priceSpan.textContent = `$${item.price.toFixed(2)}`;

    detailsDiv.appendChild(nameSpan);
    detailsDiv.appendChild(priceSpan);
    listItem.appendChild(img);
    listItem.appendChild(detailsDiv);
    menuList.appendChild(listItem);
});

document.getElementById('chatbot-button').addEventListener('click', () => {
    const chatbot = document.getElementById('chatbot');
    const isVisible = chatbot.style.transform === 'scale(1)';
    chatbot.style.transform = isVisible ? 'scale(0)' : 'scale(1)';
});
