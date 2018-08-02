
var DragExt = {};

DragExt.draggableClass = "dxt-default-draggable";
DragExt.droppableClass = "dxt-default-droppable";
DragExt.delegate = null;
DragExt.transientObject = null;

DragExt.getActualTarget = function(target)
{
    var target = $(target);

    while( ! target.hasClass( DragExt.droppableClass ) )
    {
        target = target.parent();
        if ( target.length == 0 )
            break;
    }

    return target
};

DragExt.getTransientObject = function()
{
    return DragExt.transientObject || DragExt.delegate.getDefaultTransientObject();
};

DragExt.init = function (inDraggableClass, inDroppableClass, inDragDelegate)
{
    DragExt.draggableClass = inDraggableClass;
    DragExt.droppableClass = inDroppableClass;
    DragExt.delegate = inDragDelegate;

    document.addEventListener("dragstart", function(theEvent)
    {
        var target = theEvent.target;
        var dataMap = DragExt.delegate.getTransferDataMap(target);
        DragExt.transientObject = DragExt.delegate.getTransientObject(target);

        for ( var type in dataMap )
        {
            theEvent.dataTransfer.setData(type, dataMap[type]);

            if( typeof( DragExt.delegate.getCustomDragImage ) !== 'undefined' )
            {
                var img = DragExt.delegate.getCustomDragImage(theEvent.target);
                if( img )
                {
                    theEvent.dataTransfer.setDragImage( img,
                       theEvent.offsetX, theEvent.offsetY );
                }
            }
        }
        DragExt.delegate.decorateForDragging(theEvent.target);
    });

    document.addEventListener("dragenter", function(theEvent)
    {
        theEvent.preventDefault();

        DragExt.getActualTarget( theEvent.target ).map(
            function()
            {
                if( DragExt.delegate.isDragAccepted(DragExt.getTransientObject(), this) )
                {
                    DragExt.delegate.decorateForDragEnter(this);
                }
            }
        );
    });

    document.addEventListener("dragover", function(theEvent)
    {
        theEvent.preventDefault();
        theEvent.stopPropagation();

        DragExt.getActualTarget( theEvent.target ).map( function()
            {
                if( DragExt.delegate.isDragAccepted(DragExt.getTransientObject(), this) )
                {
                    DragExt.delegate.decorateForDragOver(this);
                }
            }
        );
    });

    document.addEventListener("dragleave", function(theEvent)
    {
        theEvent.preventDefault();
        theEvent.stopPropagation();

        DragExt.getActualTarget( theEvent.target ).map(
            function()
            {
                if( DragExt.delegate.isDragAccepted(DragExt.getTransientObject(), this) )
                {
                    DragExt.delegate.decorateForDragLeave(this);
                }
            }
        );
    });

    document.addEventListener("drop", function(theEvent)
    {
        theEvent.preventDefault();
        theEvent.stopPropagation();

        DragExt.getActualTarget( theEvent.target ).map(
            function()
            {
                var transientObject = DragExt.getTransientObject();
                if( DragExt.delegate.isDragAccepted( transientObject, this ) )
                {
                    DragExt.delegate.decorateForDrop( this );
                    DragExt.delegate.handleDropDataTransfer(
                        theEvent.dataTransfer, transientObject, this );
                }
            }
        );

        DragExt.transientObject = null;
    });

    document.addEventListener("dragend", function(theEvent)
    {
        DragExt.transientObject = null;
    });

};

