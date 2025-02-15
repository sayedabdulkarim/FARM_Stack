from app.db import Wishlist, serializeList, serializeDict
from app.log_manager import logger
from bson import ObjectId
from app.db import Product


async def fetch_wishlist(user):
    wishlists = serializeList(Wishlist.find({'user_id': user['_id']}))
    for wishlist in wishlists:
        product = None
        if ObjectId.is_valid(wishlist['product_id']):
            product = Product.find_one({'_id': ObjectId(wishlist['product_id'])}, {"id": False})
            # del product['id']
        wishlist['product'] = serializeDict(product) if product else None
    return serializeList(wishlists)


async def create_wishlist(user, data):
    existing_wishlist = Wishlist.find_one(
        {'user_id': user['_id'], 'product_id': data.product_id})

    if not existing_wishlist:
        new_wishlist = Wishlist.insert_one({
            'user_id': user['_id'],
            'product_id': data.product_id,
            'created_at': data.created_at,
            'updated_at': data.updated_at,
        })
        wishlist = Wishlist.find_one({'_id': new_wishlist.inserted_id})
        return serializeDict(wishlist)
    return serializeDict(existing_wishlist)


async def delete_wishlist(user, wishlist_id):
    print(wishlist_id, 'wishlist_idddddd')
    query = {'_id': ObjectId(wishlist_id), 'user_id': user['_id']}
    found = Wishlist.find_one(query)
    if not found:
        return False
    Wishlist.delete_one(query)
    return True


async def edit_wishlist(user, wishlist_id, data):
    """
    Edit a wishlist item for a user
    
    Args:
        user (dict): User document
        wishlist_id (str): ID of wishlist to edit
        data (WishlistModel): Updated wishlist data
    
    Returns:
        dict: Updated wishlist document or None if not found
    """
    try:
        # Verify wishlist exists and belongs to user
        query = {'_id': ObjectId(wishlist_id), 'user_id': user['_id']}
        existing_wishlist = Wishlist.find_one(query)
        
        if not existing_wishlist:
            logger.warning(f"Wishlist {wishlist_id} not found for user {user['_id']}")
            return None
            
        # Update fields
        update_data = {
            'product_id': data.product_id,
            'updated_at': data.updated_at
        }
        
        # Perform update
        result = Wishlist.update_one(
            query,
            {'$set': update_data}
        )
        
        if result.modified_count:
            updated_wishlist = Wishlist.find_one(query)
            logger.info(f"Wishlist {wishlist_id} updated successfully")
            return serializeDict(updated_wishlist)
        
        logger.warning(f"No changes made to wishlist {wishlist_id}")
        return serializeDict(existing_wishlist)
        
    except Exception as e:
        logger.error(f"Error updating wishlist: {str(e)}")
        raise e
